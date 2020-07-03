library(R.matlab)
library(RateRate)
#source('ana/TwoRateModel.R')

# library("extrafont")
# loadfonts(device="pdf")
# 
library(svglite)

readParticipantData <- function(ppno) {
  
  # matfile <- readMat(sprintf('exp/Data/TwoRate_p%03d.mat', ppno))
  # cfg <- matfile$cfg[,,1]
  # 
  # mainschedules <- cfg$mainschedules
  # mainschedules <- c(mainschedules[[1]][[1]], mainschedules[[2]][[1]])
  # mainschedules <- matrix(mainschedules, ncol=2, byrow=T, dimnames=list(c(),c('trainingduration', 'traininggradual')))
  
  reaches <- read.csv(sprintf('exp/Data/TwoRate_p%03d.csv', ppno))
  
  return(list('mainschedules'=NA, 'reaches'=reaches))
  
}

getParticipantReachDeviations <- function(ppno) {
  
  rawdata       <- readParticipantData(ppno)
  reaches       <- rawdata[['reaches']]
  #mainschedules <- rawdata[['mainschedules']]
  
  tpb <- aggregate(trialno ~ blockno, data=reaches, FUN=max)
  rpb <- aggregate(rotation ~ blockno, data=reaches, FUN=mean)
  
  #durations <- mainschedules[,1]
  part1blocks <- c(2,3,4,5)
  part2blocks <- c(6,7,8,9)
  
  if (tpb$trialno[3] == 48) {
    part2blocks <- part2blocks + 2
  }
  
  trainingduration <- c(tpb$trialno[3], tpb$trialno[part2blocks[2]])
  
  traininggradual <- as.numeric(abs(c(rpb$rotation[c(part1blocks[2],part2blocks[2])])) < 30)
  
  mainschedules <- data.frame(trainingduration, traininggradual)
  
  print(mainschedules)
  
  # normalize it, split it to conditions and label it
  part1 <- getFileReachDeviations(reaches[which(reaches$blockno %in% part1blocks),])
  part2 <- getFileReachDeviations(reaches[which(reaches$blockno %in% part2blocks),])
  
  part1 <- normalizePart(part1)
  part2 <- normalizePart(part2)
  
  return(list(list('reaches'=part1, 'training'=mainschedules[1,]),
              list('reaches'=part2, 'training'=mainschedules[2,])))
  
}

getFileReachDeviations <- function(df) {
  
  block              <- c()
  trial              <- c()
  targetangle_deg    <- c()
  rotation_deg       <- c()
  reachdeviation_deg <- c()
  errorclamp         <- c()
  
  for (blockno in unique(df$blockno)) {
    
    trialnos <- unique(df$trialno[which(df$blockno == blockno)])
    
    for (trialno in trialnos) {
      
      trialdf <- df[which(df$blockno == blockno & df$trialno == trialno),]
      
      if (trialdf$feedback[1] == 2) {
        trialdf$rotation <- 0
      }
      
      trialangles <- getTrialReachAngleAt(trialdf, location='pt40')
      
      block              <- c(block,              blockno)
      trial              <- c(trial,              trialno)
      targetangle_deg    <- c(targetangle_deg,    trialangles[2])
      rotation_deg       <- c(rotation_deg,       trialdf$rotation[1])
      reachdeviation_deg <- c(reachdeviation_deg, trialangles[1])
      errorclamp         <- c(errorclamp,         (trialdf$feedback[1] == 2))
      
    }
    
  }
  
  return(data.frame(block, trial, targetangle_deg, rotation_deg, reachdeviation_deg, errorclamp))
  
}

rotateTrajectory <- function(X,Y,angle) {
  
  # create rotation matrix to rotate the X,Y coordinates
  th <- (angle/180) * pi
  R <- t(matrix(data=c(cos(th),sin(th),-sin(th),cos(th)),nrow=2,ncol=2))
  
  # put coordinates in a matrix as well
  coordinates <- matrix(data=c(X,Y),ncol=2)
  
  # rotate the coordinates
  Rcoordinates <- coordinates %*% R
  
  # return the rotated reach
  return(Rcoordinates)
  
}


getTrialReachAngleAt <- function(trialdf, location='pt40') {
  
  # location (string) determines where the angle of thereach is determines, it is one of:
  # maxvel: maximum velocity (default)
  # endpoint: end of the reach
  # cmX: the last sample before this distance from home, where X is replaced by a numeral
  # ptX: percentage distance to target, where X is a numeral (0-100)
  
  # return a matrix of two numbers:
  reachangle = matrix(data=NA,nrow=1,ncol=2)
  
  angle <- trialdf[1,'target_angle']
  X <- trialdf$Xmouse
  Y <- trialdf$Ymouse
  
  # rotate the trajectory
  # (this avoids problems in the output of atan2 for large angles)
  trajectory <- rotateTrajectory(X,Y,-1*angle)
  X <- trajectory[,1]
  Y <- trajectory[,2]
  
  # now try find the specified location in this reach:
  # if we can't find it, we need to know
  invalidlocation <- TRUE
  
  # maximum velocity, should be in the data
  if (location == 'maxvel') {
    rown <- which(MV == 1)
    if (length(rown) > 1) {
      rown <- rown[1]
    }
    if (length(rown) == 0) {
      # no maximum velocity defined!
      return(reachangle)
    }
    invalidlocation <- FALSE
  }
  # end point, just the last point in the selected stretch of the reach
  if (location == 'endpoint') {
    rown <- length(X)
    invalidlocation <- FALSE
  }
  # cutoff in centimers, the last sample before this cutoff distance is reached
  # this assumes that people don't go back, or that there is only one movement from home to target
  if (substring(location,1,2) == 'cm') {
    distance <- as.numeric(substring(location, 3))
    
    # get the distance from home:
    dist <- sqrt(X^2 + Y^2)
    
    # if there are no selected samples below 3 cm: return NAs
    if (length(which(dist > distance)) == 0) {
      return(reachangle)
    }
    
    # find the first sample, where dist > X cm
    rown <- min(which(dist > distance))
    invalidlocation <- FALSE
  }
  
  # cutoff at a percentage from home to target in whatever unit is used
  if (substring(location,1,2) == 'pt') {
    distance <- as.numeric(substring(location, 3))/100
    distance <- distance * sqrt(trialdf$Xtarget[1]^2 + trialdf$Ytarget[1]^2)
    
    # get the distance from home:
    dist <- sqrt(X^2 + Y^2)
    
    # if there are no selected samples above 3 cm: return NAs
    if (length(which(dist > distance)) == 0) {
      return(reachangle)
    }
    
    # find the first sample, where dist > X
    rown <- min(which(dist > distance))
    invalidlocation <- FALSE
  }
  
  
  # if we don't have a valid location, we can't calculate an angle to return
  if (invalidlocation) {
    return(reachangle)
  }
  
  # calculate the angle at that point for the rotated trajectory
  # this is the angular deviation we are looking for
  angulardeviation <- (atan2(Y[rown],X[rown]) / pi) * 180
  
  # put the result in the little matrix:
  reachangle[1,1] <- angulardeviation
  reachangle[1,2] <- angle
  
  return(reachangle)
  
}

normalizePart <- function(part) {
  
  part$block <- part$block - part$block[1] + 1
  
  if (rev(part$rotation[which(part$block == 2)])[1] > 0) {
    
    part$rotation_deg       <- -1 * part$rotation_deg
    part$reachdeviation_deg <- -1 * part$reachdeviation_deg
    
  }
  
  alignedtrials <- length(which(part$block == 1))
  baseline <- part[c(ceiling(alignedtrials/2):alignedtrials),]
  biases <- aggregate(reachdeviation_deg ~ targetangle_deg, data=baseline, FUN=median, na.rm=TRUE)
  
  for (targetangle in biases$targetangle_deg) {
    
    bias <- biases$reachdeviation_deg[which(biases$targetangle_deg == targetangle)]
    indices <- which(part$targetangle_deg == targetangle)
    part$reachdeviation_deg[indices] <- part$reachdeviation_deg[indices] - bias
    
  }
  
  part$rotation_deg[which(part$errorclamp)] <- NA
  
  return(part)
  
}

removeOutliers <- function(V, stds=3) {
  
  avg <- mean(V, na.rm=T)
  std <- sd(V, na.rm=T)
  
  idx <- which(abs(V-avg) > (stds*std))
  
  if (length(idx) > 0) {
    V[idx] <- NA
  }
  
  return(V)
  
}


getAllReachDeviations <- function(ppnos) {
  
  conditiondata <- list()
  
  for (ppno.idx in c(1:length(ppnos))) {
    
    ppno <- ppnos[ppno.idx]
    cat(sprintf('participant: %d ( %d / %d )\n', ppno, ppno.idx, length(ppnos)))
    data <- getParticipantReachDeviations(ppno)
    
    for (partno in c(1:length(data))) {
      
      part     <- data[[partno]]
      reaches  <- part[['reaches']]
      training <- part[['training']]
      
      if (training[['trainingduration']] == 48) {
        duration <- 'short'
      } else if (training[['trainingduration']] == 100) {
        duration <- 'long'
      }
      
      if (training['traininggradual'] == 0) {
        introduction <- 'abrupt'
      } else if (training[['traininggradual']] == 1) {
        introduction <- 'gradual'
      }
      
      condition <- sprintf('%s-%s',duration,introduction)
      
      if (!(condition %in% names(conditiondata))) {
        # make the data frame:
        block    <- reaches$block
        trial    <- reaches$trial
        schedule <- reaches$rotation_deg
        
        conditiondata[[condition]] <- data.frame(block, trial, schedule)
      }
      
      # add the data to the data frame:
      conditiondata[[condition]][sprintf('p%03d',ppno)] <- reaches$reachdeviation_deg
      
    }
    
  }
  
  return(conditiondata)
  
}

plotReachData <- function(ppnos,output='pdf') {
  
  data <- getAllReachDeviations(ppnos)
  
  allreaches <- list()
  allschedules <- list()
  alltitles <- list()
  
  # plot the reach data:
  
  if (output == 'pdf') {
    pdf(file='doc/Figures.pdf', width=8, height=6, family='ArialMT')
  }
  if (output == 'svg') {
    svglite::svglite(file='doc/Fig1_data.svg', width=8, height=6, system_fonts=list(sans="Arial") )
  }
  
  # this should be done smarter maybe:
  par(mfrow=c(2,2), las=2, mar=c(5,4,2,0.5))
  
  cat('clean and plot reach data...\n')
  
  for (conditionname in names(data)) {
    
    condition <- data[[conditionname]]
    
    trialinfo <- getTrialInfo(condition$schedule)
    schedule <- trialinfo[['schedule']]
    
    reaches <- clearReaches(condition)
    condition[,4:dim(condition)[2]] <- reaches
    write.csv(format(condition, digits=4), file=sprintf('data/tworate_%s.csv',conditionname), quote=F, row.names=F)
    
    N <- dim(as.matrix(reaches))[2]
    reversalProperties <- strsplit(conditionname,'-')
    duration <- reversalProperties[[1]][1]
    scheme <- reversalProperties[[1]][2]
    
    maintitle <- sprintf('%s %s training (N=%d)',duration,scheme,N)
    
    plot(NA,NA,main=maintitle,xlab='trial',ylab='angular deviation [°]',xlim=c(1,max(schedule$X)), ylim=c(-40,40),axes=F)
    
    scheduLength <- length(schedule$X)
    lines(x=schedule$X[c(1:(scheduLength-1))],
          y=-1*schedule$Y[c(1:(length(schedule$Y)-1))],
          col=rgb(.5,.5,.5), 
          lty=1, 
          lw=2)
    lines(x=schedule$X[c((scheduLength-1):(scheduLength))], 
          y=-1*schedule$Y[c((length(schedule$Y)-1):length(schedule$Y))], 
          col=rgb(.5,.5,.5), 
          lty=2, 
          lw=2)
    
    for (ppid in c(1:dim(reaches)[2])) {
      lines(reaches[,ppid],col='#ff82002f',lty=1,lw=0.5)
      # # lines(reaches[,ppid],col='#0fd2e22f',lty=1,lw=0.5)
    }
    
    medreaches <- apply(reaches, c(1), FUN=median, na.rm=TRUE)
    reachesCI <- apply(reaches, c(1), FUN=getCI, CI=95, measure=median, resamples=1000)
    polygon(x=c(1:length(medreaches),rev(1:length(medreaches))), y=c(reachesCI[1,],rev(reachesCI[2,])), border=NA, col='#e516364f')
    lines(medreaches, col='#e51636ff', lw=2, lty=1)
    
    axis(side=2,at=c(-30,0,30), cex.axis=0.8)
    axis(side=1,at=trialinfo[['ticks']], cex.axis=0.8)
    
    # store data for modeling:
    
    allschedules[[conditionname]] <- condition$schedule
    allreaches[[conditionname]] <- medreaches
    alltitles[[conditionname]] <- maintitle
    
  }
  
  if (output == 'svg') {
    dev.off()
    # make plot with models
    svglite::svglite(file='doc/Fig2_models.svg', width=8, height=6, system_fonts=list(sans="Arial") )
  }
  #if (output == 'pdf') {
  #  pdf(file='doc/Fig2_models.pdf', width=8, height=6, family="ArialMT" )
  #}
  
  par(mfrow=c(2,2), las=2, mar=c(5,4,2,0.5))

  for (conditionno in c(1:length(names(data)))) {
    
    cat(sprintf('fitting two-rate model (%d / %d)\n',conditionno,length(names(data))))
    
    conditionname <- names(data)[conditionno]

    condition <- data[[conditionname]]

    trialinfo <- getTrialInfo(condition$schedule)
    schedule <- trialinfo[['schedule']]
    maintitle <- alltitles[[conditionname]]

    plot(NA,NA,main=maintitle,xlab='trial',ylab='angular deviation [°]',xlim=c(1,max(schedule$X)), ylim=c(-40,40),axes=F)
    
    lines(x=schedule$X[c(1:(length(schedule$X)-1))], y=-1*schedule$Y[c(1:(length(schedule$Y)-1))], col=rgb(.5,.5,.5), lty=1, lw=2)
    lines(x=4+schedule$X[c((length(schedule$X)-1):length(schedule$X))], y=-1*schedule$Y[c((length(schedule$Y)-1):length(schedule$Y))], col=rgb(.5,.5,.5), lty=2, lw=2)

    reaches <- allreaches[[conditionname]]
    schedule <- allschedules[[conditionname]]
    
    # switching to newer model implementation:
    
    #parameters <- fitTwoRateReachModel(reaches, schedule, oneTwoRates = 2, verbose = FALSE,
    #                           grid = "skewed", gridsteps = 9, checkStability = TRUE, method = "NM",
    #                           fnscale = 1)
    
    parameters <- SMCL::twoRateFit(schedule=schedule, reaches=reaches, gridpoints=8, gridfits=6)

    #tworatemodel <- twoRateReachModel(parameters, schedule)
    
    tworatemodel <- SMCL::twoRateModel(par=parameters, schedule=schedule)

    lines(tworatemodel$total, col='#e51636ff', lw=2, lty=1)
    lines(tworatemodel$slow,  col='#ff8200ff', lw=1, lty=1)
    lines(tworatemodel$fast,  col='#c400c4ff', lw=1, lty=1)

    axis(side=2,at=c(-30,0,30), cex.axis=0.8)
    axis(side=1,at=trialinfo[['ticks']], cex.axis=0.8)

  }
  
  if (output %in% c('svg','pdf')) {
    dev.off()
  }
  
  
}

getTrialInfo <- function(schedule) {
  
  # this only works for abrupt schedules!
  
  # perhaps for gradual we need to set some minimal deviation
  # that works two ways:
  # 1) whenever we start to get small, non-zero deviations: ignore
  # 2) whenever they return to exactly zero: add a phase-border
  
  gradual <- FALSE
  
  X <- c(1)
  Y <- c(schedule[1])
  ticklocations <- c(1)
  
  for (trialno in c(2:length(schedule))) {
    
    deviation <- schedule[trialno]
    
    #cat(sprintf('\n *** next trial, with deviation: %f\n', deviation))
    
    if (is.na(deviation)) {
      
      #print('NA: considering this the end, finishing up...')
      
      # this should be the last phase,
      # so we finish up everything and return
      X <- c(X, trialno-1, trialno-1, length(schedule))
      Y <- c(Y, Y[length(Y)], 0, 0)
      ticklocations <- c(ticklocations,trialno-1,length(schedule))
      
      # for more complicated schedules; adapt this to find the next non-NA value 
      return(list('schedule'=list('X'=X,'Y'=Y), 'ticks'=ticklocations))
      
    }
    
    if (abs(deviation - schedule[trialno-1]) > 2)  {
      
      #print('large change...')
      
      X <- c(X, trialno-1, trialno-1)
      Y <- c(Y, Y[length(Y)], deviation)
      ticklocations <- c(ticklocations,trialno-1)
      
      gradual <- FALSE
      
    } else if (!gradual & abs(deviation - schedule[trialno-1]) > 0) {
      
      #cat('small change, starting gradual?\n')
      
      X <- c(X, trialno-1)
      Y <- c(Y, Y[length(Y)])
      ticklocations <- c(ticklocations,trialno-1)
      
      gradual <- TRUE
      
    } else if (abs(deviation - schedule[trialno-1]) == 0 & gradual) {
      
      #cat('NO change, stopping gradual?\n')
      
      X <- c(X, trialno-1)
      Y <- c(Y, deviation)
      ticklocations <- c(ticklocations,trialno-1)
      
      gradual <- FALSE
      
    }
    
  }
  
  return(list('schedule'=list('X'=X,'Y'=Y), 'ticks'=ticklocations))
  
}

clearReaches <- function(df) {
  
  # first three columns are not necessary:
  
  reaches <- as.matrix(df[,c(4:dim(df)[2])])
  
  # here we remove obviously incorrect reaches:
  reaches[which(abs(reaches) > 60)] <- NA
  
  # we also want to remove outliers,
  # but only if there are 4 or more participants
  
  if (dim(reaches)[2] > 3) {
    
    for (trialno in c(1:dim(reaches)[1])) {
      
      reaches[trialno,] <- removeOutliers(reaches[trialno,], stds=2)
      
    }
    
  }
  
  return(reaches)
  
}

getCI <- function(V, CI=95, resamples=1000, measure=median) {
  
  V <- V[is.finite(V)]
  
  BS <- apply(matrix(sample(V,size=length(V)*resamples,replace=TRUE), nrow=1000), c(1), measure)
  
  return(quantile(BS,probs=c((100-CI)/200,1-((100-CI)/200))))
  
}


plotPosterReachData <- function(ppnos) {
  
  data <- getAllReachDeviations(ppnos)
  
  allreaches <- list()
  allschedules <- list()
  alltitles <- list()
  
  # plot the reach data:
  
  pdf(file='doc/Figures.pdf', width=8, height=6)
  
  #svglite(file='doc/posterFig.svg', width=8, height=6, system_fonts=list(sans="Arial") )
  
  # this should be done smarter maybe:
  par(mfrow=c(2,2), las=2, mar=c(5,4,2,0.5))
  
  cat('clean and plot reach data...\n')
  
  for (conditionno in c(1:length(names(data)))) {
    
    conditionname <- names(data)[conditionno]
    condition <- data[[conditionname]]
    
    trialinfo <- getTrialInfo(condition$schedule)
    schedule <- trialinfo[['schedule']]
    
    reaches <- clearReaches(condition)
    condition[,4:dim(condition)[2]] <- reaches
    write.csv(format(condition, digits=4), file=sprintf('data/tworate_%s.csv',conditionname), quote=F, row.names=F)
    
    N <- dim(as.matrix(reaches))[2]
    reversalProperties <- strsplit(conditionname,'-')
    magnitude <- reversalProperties[[1]][1]
    duration <- reversalProperties[[1]][2]
    
    maintitle <- sprintf('%s and %s (N=%d)',magnitude,duration,N)
    
    plot(NA,NA,main=maintitle,xlab='trial',ylab='angular deviation [°]',xlim=c(1,max(schedule$X)), ylim=c(-40,40),axes=F)
    
    scheduLength <- length(schedule$X)
    lines(x=schedule$X[c(1:(scheduLength-1))],
          y=-1*schedule$Y[c(1:(length(schedule$Y)-1))],
          col=rgb(.5,.5,.5), 
          lty=1, 
          lw=2)
    lines(x=schedule$X[c((scheduLength-1):(scheduLength))], 
          y=-1*schedule$Y[c((length(schedule$Y)-1):length(schedule$Y))], 
          col=rgb(.5,.5,.5), 
          lty='dotted', 
          lw=2)
    
    
    for (ppid in c(1:dim(reaches)[2])) {
      lines(reaches[,ppid],col='#ff82002f',lty=1,lw=0.5)
      # # lines(reaches[,ppid],col='#0fd2e22f',lty=1,lw=0.5)
    }
    
    medreaches <- apply(reaches, c(1), FUN=median, na.rm=TRUE)
    reachesCI <- apply(reaches, c(1), FUN=getCI, CI=95, measure=median, resamples=1000)
    polygon(x=c(1:length(medreaches),rev(1:length(medreaches))), y=c(reachesCI[1,],rev(reachesCI[2,])), border=NA, col='#e516364f')
    lines(medreaches, col='#e51636ff', lw=2, lty=1)
    
    axis(side=2,at=c(-30,0,30), cex.axis=0.8)
    axis(side=1,at=trialinfo[['ticks']], cex.axis=0.8)
    
    # store data for modeling:
    
    allschedules[[conditionname]] <- condition$schedule
    allreaches[[conditionname]] <- medreaches
    alltitles[[conditionname]] <- maintitle
    
  }
  #
  #dev.off()
  #  
  ## make plot with models
  #
  #svglite(file='doc/Fig2_models.svg', width=8, height=6, system_fonts=list(sans="Arial") )
  #
  ## pdf(file='doc/Fig2_models.pdf', width=8, height=6, family="Arial" )
  #
  #par(mfrow=c(2,2), las=2, mar=c(5,4,2,0.5))
  #
  for (conditionno in c(1:length(names(data)))) {
    
    cat(sprintf('fitting two-rate model (%d / %d)\n',conditionno,length(names(data))))
    
    conditionname <- names(data)[conditionno]
    
    condition <- data[[conditionname]]
    
    trialinfo <- getTrialInfo(condition$schedule)
    schedule <- trialinfo[['schedule']]
    maintitle <- alltitles[[conditionname]]
    
    plot(NA,NA,main=maintitle,xlab='trial',ylab='angular deviation [°]',xlim=c(1,max(schedule$X)), ylim=c(-40,40),axes=F)
    
    lines(x=schedule$X[c(1:(length(schedule$X)-1))], y=-1*schedule$Y[c(1:(length(schedule$Y)-1))], col=rgb(.5,.5,.5), lty=1, lw=2)
    lines(x=schedule$X[c((length(schedule$X)-1):length(schedule$X))], y=-1*schedule$Y[c((length(schedule$Y)-1):length(schedule$Y))], col=rgb(.5,.5,.5), lty='dotted', lw=2)
    
    reaches <- allreaches[[conditionname]]
    schedule <- allschedules[[conditionname]]
    
    parameters <- fitTwoRateReachModel(reaches, schedule, oneTwoRates = 2, verbose = FALSE,
                                       grid = "skewed", gridsteps = 9, checkStability = TRUE, method = "NM",
                                       fnscale = 1)
    
    tworatemodel <- twoRateReachModel(parameters, schedule)
    
    lines(tworatemodel$total, col='#e51636ff', lw=2, lty=1)
    lines(tworatemodel$slow,  col='#ff8200ff', lw=1, lty=1)
    lines(tworatemodel$fast,  col='#c400c4ff', lw=1, lty=1)
    
    axis(side=2,at=c(-30,0,30), cex.axis=0.8)
    axis(side=1,at=trialinfo[['ticks']], cex.axis=0.8)
    
  }
  
  dev.off()
  
  
}

 
