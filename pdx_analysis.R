library("plyr")

d <- read.csv(file="phenodata.csv",sep=",",header=TRUE,stringsAsFactors = FALSE,row.names=1)
d$Adverse_ICD9_simple <- gsub ("causing adverse effect in therapeutic use","",d$Adverse_ICD9)
d$Adverse_ICD9_simple <- strtrim(d$Adverse_ICD9_simple,50)
d$DX_Name_simple <- gsub ("causing adverse effect in therapeutic use","",d$DX_Name)
d$DX_Name_simple <- strtrim(d$DX_Name_simple,50)

d10 <- d[ d$Adverse_ICD9 %in% names(table(d$Adverse_ICD9))[table(d$Adverse_ICD9) >10],]
dx10 <- d[ d$DX_Name %in% names(table(d$DX_Name))[table(d$DX_Name) >10],]
png("adverse_hist.png",width = 8.5, height=11, units="in",res=150)
par(mar=c(20,8,8,2))
plot(sort(decreasing = TRUE,table(d$Adverse_ICD9_simple))[1:30],las=3,yaxt="n",ylab="")
title(main="Frequency of Adverse ICD (Top 30)", ylab="Frequency", line=3)
axis(2,las=2)
dev.off()


png("adverse_boxplot_cost.png",width = 8.5, height=11, units="in",res=150)
par(mar=c(20,8,8,2))
boxplot(as.numeric(Total_Charges)~Adverse_ICD9_simple,data=d10,yaxt="n",las=3)
title(main="Adverse ICD9 with > 10 events", ylab="Total Charges", line=5)
axis(2,las=2)
dev.off()

png("dx_boxplot_cost.png",width = 8.5, height=11, units="in",res=150)
par(mar=c(20,8,8,2))
boxplot(as.numeric(Total_Charges)~DX_Name_simple,data=dx10,yaxt="n",las=3)
title(main="Adverse ICD9 with > 10 events", ylab="Total Charges", line=5)
axis(2,las=2)
dev.off()
png("adverse_boxplot_los.png",width = 8.5, height=11, units="in",res=150)
par(mar=c(20,8,8,2))
boxplot(as.numeric(LOS)~Adverse_ICD9_simple,data=d10,yaxt="n",las=3)
title(main="Adverse ICD9 with > 10 events", ylab="Length of Stay", line=5)
axis(2,las=2)
dev.off()

drug <- read.csv(file="drug_data.csv",sep=",",header=TRUE,stringsAsFactors = FALSE,row.names = 1)
drug20 <- drug[,(colSums(drug)) >20]
d<- ddply(d,'Adverse_ICD9', transform, median = median(Total_Charges))
d$expensive <- ifelse(d$Total_Charges>d$median, 'YES', 'NO')

#subset to Antineoplastic and immunosuppressive drugs
drugAIds <- subset(d, d$Adverse_ICD9_simple == "Antineoplastic and immunosuppressive drugs ")
drugsub <- drug20[rownames(drug20) %in% rownames(drugAIds),]
drugsub <- drugsub[,apply(drugsub, 2, var, na.rm=TRUE) >= .25]
drug.pca <- prcomp(drugsub, scale = FALSE)
ggbiplot(drug.pca)
