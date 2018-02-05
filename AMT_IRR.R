

#### SETUP: RUN THESE EVERY TIME ####

wants <- c("DescTools", "irr","psych")
has   <- wants %in% rownames(installed.packages())
if(any(!has)) install.packages(wants[!has])

library(irr)
library(psych)
library(ICC)

batch = "batch5" ## CHANGE THIS FOR THE END OF YOUR FOLDER NAME (WoZ_test1)

directory = paste("R_output_",batch, sep = "", collapse = NULL)
print(directory)
getwd()
setwd(directory)  



temp = list.files(pattern="irr")
for (i in 1:length(temp)) assign(temp[i], read.csv(temp[i],header=T))

df.list <- list()

for (i in 1:length(temp)){ 
  z <- i
  file <- paste("irr", z, ".csv", sep="")
  new <- get(paste("irr", z, ".csv", sep=""))
  df.list[[file]] <-new
}

print(df.list)




#######################################################




#### BEST 4 RATERS #####

### Find ICC
dfList1 <- lapply(df.list, function(df) {
  icc(df, model = "twoway", type = "consistency", unit = "single")[7]
})


## Krippendorff's Alpha
dfList2 <- lapply(df.list, function(df) {
  kripp.alpha(t(df), method="ordinal")[5]
})


## Cronbach's Alpha
dfList3 <- lapply(df.list, function(df) {
  a <- alpha(df)[[1]]
  a[1]
})




### Output best 4 to csv ###
completeList <- mapply(c, dfList1, dfList2, dfList3, SIMPLIFY=FALSE)
completeList

completeList <- do.call(rbind, lapply(seq_along(completeList), function(i){
  data.frame(CLUSTER=i, completeList[[i]])
}))

outname = paste("Rapport_AMT_IRR_", batch, "_All-4-raters.csv", sep="", collapse = NULL)
write.table(as.data.frame(completeList),file=outname, col.names = NA, sep=",")











#######################################################


###### Best 3 raters ###### 


krippList <- list()
iccList <- list()
fileList <- list()
a=-1
for (amt in df.list){
  
  a = a + 1
  maxKA = -150
  maxIC = -150
  print("amt")
  print(a)
  
  for (i in 1:ncol(amt)) {
    
    for (j in 1:ncol(amt)){
      for (k in 1:ncol(amt)){
        
        
        if (i!=j && i!=k && j!=k){
          count1 = i
          count2 = j
          count3 = k
          
          pair <- amt[c(count1,count2,count3)]
          print(pair)
          print("Checking")
          print(count1)
          print(count2)
          print(count3)
          cols = c(count1,count2,count3)
          print(cols)
          KA <- kripp.alpha(t(pair), method="ordinal")[5]
          KA <- as.numeric(KA)
          
          ic <- icc(pair, model = "twoway", type = "consistency", unit = "single")[7]
          ic <- as.numeric(ic)
          
          print(KA)
          print(ic)
          # print(CA)
          if (KA > maxKA) {
            maxKA = KA
            print("maxKA:")
            print(maxKA)
            col_kripp = list(cols,maxKA)
            print("colKripp:")
            print(col_kripp)
          }
          
          if (ic > maxIC) {
            maxIC = ic
            print("maxIC:")
            print(maxIC)
            col_ICC = list(cols,maxIC)
            print("col_ICC:")
            print(col_ICC)
          }
        }
        
      }
    }
  }
  print("maxKA")
  print(maxKA)
  print("maxIC")
  print(maxIC)

  file = paste("amt",a,sep="")
  fileList[[length(fileList)+1]] <- list(file)
  krippList[[length(krippList)+1]] <- list(maxKA)
  iccList[[length(iccList)+1]] <- list(maxIC)
  
}


## Output 3 way KA and ICC to csv:
# KA
write.table(as.data.frame(krippList),file="Rapport_AMT_IRR_Batch5_best-3-raters_kripp.csv", col.names = NA, sep=",")

# ICC
write.table(as.data.frame(iccList),file="Rapport_AMT_IRR_Batch5_best-3-raters_ICC.csv", col.names = NA, sep=",")




####
#completeList_3way <- mapply(c, fileList, krippList, SIMPLIFY=FALSE)
#completeList_3way
#completeList_3way <- do.call(rbind, lapply(seq_along(completeList_3way), function(i){
 # data.frame(CLUSTER=i, completeList_3way[[i]])
#}))









