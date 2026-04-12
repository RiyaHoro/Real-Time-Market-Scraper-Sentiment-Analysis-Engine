library(syuzhet)

args <- commandArgs(trailingOnly=TRUE)

reviews <- unlist(strsplit(args[1], "\\|"))

sentiment <- get_sentiment(reviews)

score <- mean(sentiment, na.rm=TRUE)

if(is.na(score)){
  score <- 0
}

cat(score)