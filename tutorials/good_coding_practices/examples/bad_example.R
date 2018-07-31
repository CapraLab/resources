# 
# June 2016
# commands to get union of eQTL tissues in HMRs
#clust <- read.delim2("~/clust_hist_over.bed", header=FALSE, stringsAsFactors=FALSE)
prev = 0
g <- c()
for (i in 1:nrow(clust)) {
  clust$s_eqtl[i] <- strsplit(clust$V5[i],",")
  if (prev == clust$V2[i]) {
     g <- c(g,i) 
     clust$un_eqtl[i] <- list(union(clust$s_eqtl[i][[1]],clust$un_eqtl[i-1][[1]]))
  } else{
    if (length(g) > 0){for (j in 1:length(g)){
      clust$un_eqtl[g[j]] <- list(sort(clust$un_eqtl[i-1][[1]]))}}
    clust$un_eqtl[i] <- list(clust$s_eqtl[i][[1]])
    g <- c(i)
  }
  prev <- clust$V2[i]
}

# grouping and filtering hmr
robust <- clust %>% group_by(V1,V2,V3,V4) %>% summarise(e_un <- unique(un_eqtl))
robust$un <- robust$`e_un <- unique(un_eqtl)`
robust <- robust[which(!is.na(robust$un)),]
robust$`e_un <- unique(un_eqtl)` <- NULL
for (i in 1:nrow(robust)) {
  if (length(robust$un[i][[1]]) == 0) {robust$un[i] <- NA}}
  #if (length(robust$h_un[i][[1]]) == 0) {robust$h_un[i] <- NA}}
robust <- robust[which(!is.na(robust$un)),]
#robust <- robust[which(!is.na(robust$h_un)),]
for (i in 1:nrow(robust)) {
  robust$e[i] <- robust$un[i][[1]][1]
  #robust$h[i] <- robust$h_un[i][[1]][1]
  for (j in 2:length(robust$un[i][[1]])){
    robust$e[i] <- paste(robust$e[i],robust$un[i][[1]][j],sep = ",")}
  if (length(robust$un[i][[1]]) == 1) {robust$e[i] <- robust$un[i][[1]][1]}
  #for (j in 2:length(robust$h_un[i][[1]])){
  #  robust$h[i] <- paste(robust$h[i],robust$h_un[i][[1]][j],sep = ",")}
  #if (length(robust$h_un[i][[1]]) == 1) {robust$h[i] <- robust$h_un[i][[1]][1]}
  #robust$hmrs[i] <- robust$h[i][[1]]
  robust$eqtls[i] <- robust$e[i][[1]]}
#write.table(robust[c(1,2,3,4,7)],file = "~/u_clust_hist.bed",quote = F, col.names = F, row.names = F, sep = "\t")

# analysis and plots
clust$type <- "Clustered"
nonclust$type <- "Non-Clustered"
summary(clust$V7)
summary(nonclust$V7)
wilcox.test(clust$V7,nonclust$V7)
p <- data.frame(sim = c(clust$V7,nonclust$V7),type=c(clust$type,nonclust$type))
ggplot(p,aes(x=type,y=sim,fill=type)) + geom_violin(color="darkgrey",alpha=0.75) + scale_fill_manual(values=c("seagreen3","royalblue4")) + geom_boxplot(width=0.05,fill="white")
