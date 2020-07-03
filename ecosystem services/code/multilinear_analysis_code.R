# R code for NERC-COVID hackathon
# This code does a multilinear regression analysis to determine the contributing factors to COVID death rate

#READ IN THE DATA

alldata3 = read.table("./data/processed/greenspace_metrics.csv",sep=",",header=TRUE,stringsAsFactors = FALSE)


greenspacefrac = alldata3$Greenspace.Fraction
greenspacesize = alldata3$Greenspace.Average.Area
parkmean = alldata3$Mobility.Parks.Average.Post.lockdown....from.baseline.
parkgrad = alldata3$Mobility.Park.Rate.of.Change.Post.lockdown.....from.baseline.per.day.
workmean = alldata3$Mobility.Workplaces.Average.Post.lockdown....from.baseline.
workgrad = alldata3$Mobility.Workplaces.Rate.of.Change.Post.lockdown.....from.baseline.per.day.
recmean = alldata3$Mobility.Retail...Recreation.Average.Post.Lockdown....from.baseline.
recgrad = alldata3$Mobility.Retail...Recreation.Rate.of.Change.Post.Lockdown....from.baseline.per.day.
resimean = alldata3$Mobility.Residential.Average.Post.Lockdown....from.Baseline.
resigrad = alldata3$Mobility.Residential.Rate.of.Change.Post.Lockdown....from.Baseline.
grocmean = alldata3$Mobility.Grocery...Pharmacy.Average.Post.Lockdown....from.baseline.
grocgrad = alldata3$Mobility.Grocery...Pharmacy.Rate.of.Change.Post.Lockdown....from.baseline.per.day.
parkgrad[parkgrad<(-1)]<-NA #these have some outliers which have missing data in the original timeseries
recgrad[recgrad<(-1)]<-NA
grocgrad[grocgrad<(-1)]<-NA

wealth = alldata3$Gross.Income.Per.Head..2018.pounds.
covid = as.numeric(alldata3$COVID.19.Death.Rate.April.May..per.100.000.)
greenspaceno = alldata3$Greenspace.Number
urbanrural = alldata3$Urbanisation
ruralness = rep(NA, length(urbanrural))
ruralness[urbanrural == "Rural"] <- 1
ruralness[urbanrural == "Urban"] <- 0


names =c("wealth","parkmean","parkgrad","recmean","recgrad","resimean","resigrad","workmean","workgrad","grocmean","grocgrad","greenspaceno","greenspacefrac","greenspacesize")

# REGRESSION WITH TWO VARIABLES, ALL DATA, ACCOUNTING FOR RURALNESS
cor(covid,ruralness,use='pairwise.complete.obs',method='pearson') -> corrural
corfac = NULL

for(name in names) {
  eval(parse( text = paste("data = ",name,sep="") ))
  lm(covid ~ ruralness+data)[[1]] -> factors
  correl = cor(covid,factors[2]*ruralness +factors[3]*data,use='pairwise.complete.obs',method='pearson')

corfac=c(corfac,correl/corrural)
}
impacts_ruralnessonly = cbind(names,corfac)

#REGRESSION WITH THREE VARIABLES, ALL DATA, ACCOUNTING FOR WEALTH AND RURALNESS
corruralwealth = as.numeric(impacts_ruralnessonly[1,2])*corrural

corfac = NULL
for(name in names[2:length(names)]) {
  
  eval(parse( text = paste("data = ",name,sep="") ))
  lm(covid ~ wealth + ruralness + data)[[1]] -> factors
  correl = cor(covid,factors[2]*wealth +factors[3]*ruralness + factors[4]*data,use='pairwise.complete.obs',method='pearson')
  
  corfac=c(corfac,correl/corruralwealth)
}
impacts_wealthrural = cbind(names[2:length(names)],corfac)


#ALTERNATIVE: REPEATING ANALYSIS WITH URBAN AND RURAL SEPARATELY=============
covid_r = covid[ruralness==1]
wealth_r = wealth[ruralness==1]
groc_r = grocmean[ruralness==1]
covid_u = covid[ruralness==0]
wealth_u = wealth[ruralness==0]
groc_u = grocmean[ruralness==0]
parks_u = parkmean[ruralness==0]

#REGRESSION WITH ONE VARIABLE, ONLY RURAL
corfac = NULL
for(name in names) {
  eval(parse( text = paste("data = ",name,"[ruralness==1]",sep="") ))
  correl = cor(covid_r,data,use='pairwise.complete.obs',method='pearson')
  
  corfac=c(corfac,correl)
}
impacts_ruralonevar = cbind(names,corfac)

#REGRESSION WITH ONE VARIABLE, ONLY URBAN
corfac = NULL
for(name in names) {
  eval(parse( text = paste("data = ",name,"[ruralness==0]",sep="") ))
  correl = cor(covid_u,data,use='pairwise.complete.obs',method='pearson')
  
  corfac=c(corfac,correl)
}
impacts_urbanonevar = cbind(names,corfac)

# REGRESSION WITH TWO VARIABLES, ONLY RURAL, ACCOUNTING FOR GROCERIES
cor(covid_r,groc_r,use='pairwise.complete.obs',method='pearson') -> corgroc_r

corfac = NULL
for(name in names) {
  eval(parse( text = paste("data = ",name,"[ruralness==1]",sep="") ))
  lm(covid_r ~ groc_r+data)[[1]] -> factors
  correl = cor(covid_r,factors[2]*groc_r +factors[3]*data,use='pairwise.complete.obs',method='pearson')
  
  corfac=c(corfac,correl/corgroc_r)
}
impacts_ruralonly = cbind(names,corfac)


# REGRESSION WITH TWO VARIABLES, ONLY URBAN, ACCOUNTING FOR WEALTH
cor(covid_u,wealth_u,use='pairwise.complete.obs',method='pearson') -> corwealth_u

corfac = NULL
for(name in names) {
  eval(parse( text = paste("data = ",name,"[ruralness==0]",sep="") ))
  lm(covid_u ~ wealth_u+data)[[1]] -> factors
  correl = cor(covid_u,factors[2]*wealth_u +factors[3]*data,use='pairwise.complete.obs',method='pearson')
  corfac=c(corfac,correl/corwealth_u)
}
impacts_urbanonly = cbind(names,corfac)

#===============================================================================
#MAKE PLOTS
pdf("./figures/correlation_coefficient_plots.pdf",width=11,height=7.5)
par(mfrow=c(3,1),mar=c(4.5,4.5,2,1))
ylm = 0.5
ymn = 0.1

plot(corrural*as.numeric(impacts_ruralnessonly[,2]),xaxt="n",ylim=c(ymn,ylm),main="ALL DATA (Multilinear regression of COVID with ruralness [=baseline] + Factor)",xlab="Factors",cex.axis=1.3,cex.lab=1.3,cex=2,pch=4,ylab="Pearson's R")
axis(1,at=1:length(impacts_ruralnessonly[,1]),labels=impacts_ruralnessonly[,1],cex.axis=0.8)
lines(c(-50,50),c(corrural,corrural)*-1,lty=2)
lines(c(-50,50),c(0.19,0.19),col='blue',lty=2)
lines(c(1,10),corrural*as.numeric(impacts_ruralnessonly[c(1,10),2]),type='p',col='red',cex=4)
legend(x='topright',legend=c("Baseline","5% significance level"),lwd=1,col=c("black","blue"),lty=2,cex=1.3)
text(x=1+0.5,y=0.42,labels="Income per capita",cex=1.3)
text(x=10,y=0.42,labels="Grocery shopping",cex=1.3)

plot(as.numeric(impacts_ruralonevar[,2]),xaxt='n',ylim=c(-ylm,ylm),main="RURAL DATA ONLY (Single correlation of COVID with Factor)",cex.axis=1.3,cex.lab=1.3,cex=2,pch=4,ylab="Pearson's R",xlab="Factors")
lines(c(-50,50),c(0.27,0.27),col='blue',lty=2)
lines(c(-50,50),c(-0.27,-0.27),col='blue',lty=2)
lines(c(-50,50),c(0,0))
lines(c(4,10),as.numeric(impacts_ruralonevar[c(4,10),2]),type='p',col='red',cex=4)
axis(1,at=1:length(impacts_ruralonevar[,1]),labels=impacts_ruralonevar[,1],cex.axis=0.8)
text(x=4,y=0.45,labels="Retail and recreation",cex=1.3)
text(x=10,y=0.45,labels="Grocery shopping",cex=1.3)

plot(corwealth_u*as.numeric(impacts_urbanonly[,2]),ylim=c(ymn,ylm),xaxt='n',main="URBAN DATA ONLY (Multilinear regression of COVID with wealth [=baseline] + Factor)",cex.axis=1.3,cex.lab=1.3,cex=2,pch=4,ylab="Pearson's R",xlab="Factors",xlim=c(2,14))
lines(c(-50,50),c(corwealth_u,corwealth_u)*-1,lty=2)
lines(c(-50,50),c(0.27,0.27),col='blue',lty=2)
lines(c(2,10),corwealth_u*as.numeric(impacts_urbanonly[c(2,10),2]),type='p',col='red',cex=4)
axis(1,at=1:length(impacts_urbanonly[,1]),labels=impacts_urbanonly[,1],cex.axis=0.9)
text(x=2+0.6,y=0.32,labels="Use of urban greenspace",cex=1.3)
text(x=10,y=0.32,labels="Grocery shopping",cex=1.3)
dev.off()

#SHOW THAT URBAN GREENSPACES REDUCE DEATH RATE:
print(lm(covid_u ~ wealth_u + groc_u + parks_u))
