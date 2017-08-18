# read data in
na.data <- na.omit(read.csv2("..//data//monthly_preferred_1.csv", sep=";", stringsAsFactors = FALSE))


e5 <- ts(na.data$e5, start = c(1978,1), frequency = 12)
num.nas <- length(window(e5, 1978, c(1992,1)))
data <- na.data[num.nas:470,]
as.numeric(data$l_pnfuel)

sample <- data.frame(cbind(as.numeric(data$l_pnfuel),
                           as.numeric(data$e5),
                           as.numeric(data$cpi),
                           as.numeric(data$l_rgdp),
                           as.numeric(data$l_dm2m)))

s_full <-  ts(cbind(as.numeric(data$l_pnfuel),
                    as.numeric(data$e5),
                    as.numeric(data$cpi),
                    as.numeric(data$l_rgdp),
                    as.numeric(data$l_dm2m)),
              start = c(1992,1), frequency = 12)

l_pnfuel <- ts(as.numeric(data$l_pnfuel), start = c(1992,1), frequency = 12)
e5 <- ts(as.numeric(data$e5), start = c(1992,1), frequency = 12)
cpi <- ts(as.numeric(data$cpi), start = c(1992,1), frequency = 12)
l_rgdp<- ts(as.numeric(data$l_rgdp), start = c(1992,1), frequency = 12)
l_dm2m <- ts(as.numeric(data$l_dm2m), start = c(1992,1), frequency = 12)

s_tri <-ts(cbind(as.numeric(data$cpi),
                 as.numeric(data$l_rgdp),
                 as.numeric(data$l_dm2m)),
           start = c(1992,1), frequency = 12)

s_pre <- window(s_full, 1992, 2004)

s_post <- window(s_full, 2005)
# libraries
# install.packages(c("seasonal", "tseries", "vars"))
# install.packages(c("fUnitRoots", "forecast"))
# install.packages("Matrix")
library(Matrix)
library(seasonal)
library(tseries)
library(vars)
#library(fUnitRoots)
library(urca) # more unit root and cointegration tests
#library(forecast)
#library(quantreg)
library(strucchange) #for endogenous break point test
# library(ggplot2)

#####################################################
########## cointegratin analysis ####################
#####################################################
# hypothesis : there are 2 permanent shocks 
# that correspond to a supply and inflation target shock
# the other shocks should be transitory
# givng a cointegration rank of at most 2

coint_full <- ca.jo(cbind(l_pnfuel, e5, l_rgdp, cpi, l_dm2m), type = "trace", ecdet = "const", K = 4, spec = "transitory")
summary(coint_full)

# I think this would confirm my hypothesis that the cointrgation rank is r=2 at the 5% level
# depending on how exact I need to know what the cointegration relation s look like, do tasts of pairs and tripplets

