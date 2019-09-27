# set working directory (see https://stackoverflow.com/a/35842119)
dir = tryCatch({
  # script being sourced
  getSrcDirectory()[1]
}, error = function(e) {
  # script being run in RStudio
  dirname(rstudioapi::getActiveDocumentContext()$path)
})
setwd(dir)

library(data.table)

training_set <- fread("training.csv", header=TRUE, sep=",", quote="\"", strip.white=TRUE, showProgress=TRUE, encoding="UTF-8", na.strings=c("", "null"), stringsAsFactors=FALSE)
nrow(training_set)
# 47,681

length(which(is.na(training_set$url)))
# 0

training_set[is.na(training_set$url)]$query
# ...

length(which(is.na(training_set$title)))
# 0

training_set[is.na(training_set$title)]$query
# ...

length(which(is.na(training_set$snippet)))
# 4

training_set[is.na(training_set$snippet)]$query
# ...


testing_set <- fread("testingUpdated.csv", header=TRUE, sep=",", quote="\"", strip.white=TRUE, showProgress=TRUE, encoding="UTF-8", na.strings=c("", "null"), stringsAsFactors=FALSE)
nrow(testing_set)
# 47,678

length(which(is.na(testing_set$url)))
# 0

length(which(is.na(testing_set$title)))
# 0

length(which(is.na(testing_set$snippet)))
# 296

testing_set[is.na(testing_set$snippet)]$query
# ...
