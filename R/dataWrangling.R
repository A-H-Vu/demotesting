

handleOneFile <- function(filename) {
  
  df <- read.csv(filename, stringsAsFactors = F)
  
  trialno <- c()
  targetangle_deg <- c()
  rotation_deg <-c()
  reachdeviation_deg <- c()
  
  
  for (trialnum in c(1:dim(df)[1])) {
    
    x <- convertCellToNumVector(df$trialMouse.x[trialnum])
    y <- convertCellToNumVector(df$trialMouse.y[trialnum])
    s <- convertCellToNumVector(df$step[trialnum])
    r <- df$rotation_deg[trialnum]
    a <- df$targetangle_deg[trialnum]
    
    # remove stuff that is not step==2
    step2idx = which(s == 2)
    x <- x[step2idx]
    y <- y[step2idx]
    
    # get first point beyond some distance
    d <- sqrt(x^2 + y^2)
    idx <- which(d > .2)[1]
    x <- x[idx]
    y <- y[idx]
    
    # get angular deviation of reach from target angle:
    theta = (-a / 180) * pi
    x = (x * cos(theta)) - (y * sin(theta))
    y = (x * sin(theta)) + (y * cos(theta))
    rd <- (atan2(y, x) / pi) * 180
    
    # store in vectors:
    trialno <- c(trialno, trialnum)
    targetangle_deg <- c(targetangle_deg, a)
    rotation_deg <-c(rotation_deg, r)
    reachdeviation_deg <- c(reachdeviation_deg, rd)

  }
  
  # vectors as data frame columns:
  dfrd <- data.frame(trialno, targetangle_deg, rotation_deg, reachdeviation_deg)
  #return(dfrd)
  
  # split into two
  # determine condition of the two halves
  
  # output:
  
  # list with 3 or 2 elements:
  
  # normalized reach deviations + normalized rotation schedules
  # for (3 or) 2 conditions?
  # these will be added to a matrix or data frame for plotting and fitting
  
}

convertCellToNumVector <- function(v) {
  
  # remove opening square bracket:
  v <- gsub('\\[', replacement='', x=v)
  # remove closing square bracket:
  v <- gsub(']', replacement='', x=v)
  # split by commas:
  v <- strsplit(v, ',')
  # convert to numeric:
  v <- lapply(v, FUN=as.numeric)
  # make vector:
  v <- as.vector(unlist(v))
  
  return(v)
  
}