# loop to test fpor serial correlation 

lm_row <- function(varest_model,H_max, type = "PT.asymptotic"){
  H = c(1:H_max)
  p_vals = c(rep(0,H_max))
  
  for (h in H){
    if (type == "BG"| type == "ES"){
      test <- serial.test(varest_model, lags.bg = h, type = type)
    }
    else {
      test <- serial.test(varest_model, lags.pt = h, type = type)
    }
    
    p_vals[h] <- test$serial$p.value
  }
  return(p_vals)
}

# read data in
na.data <- na.omit(read.csv2("..//data//keating_bel.csv", sep=";", stringsAsFactors = FALSE))


e5 <- ts(na.data$e5, start = c(1978,1), frequency = 12)
num.nas <- length(window(e5, 1978, c(1992,1)))
var_list <- names(na.data)

data <- na.data[num.nas:462,]

var_names <- c('l_gdpdef', 'l_gdp', 'l_pnfuel', 'u_dm2m', 'l_dm2m')
sample <- data[, var_names]
s_full <- ts(sample, start = c(1992,1), frequency = 12)

s_pre <- window(s_full, 1992, 2007)

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

#######################################################
############ full smaple analysis#####################
#######################################################

lags <- VARselect(s_pre, lag.max = 20)$selection[1]
lags
mod1 <- VAR(s_full, p = 4, type = "const")
p_vals <- lm_row(mod1, H_max=18, "BG")
p_vals

serial.test(mod1, lags.pt = 18, type = "PT.asymptotic")
serial.test(mod1, lags.pt = 18, type = "PT.adjusted")

Sig <- mod_s_full$obs
#summary(mod_s_full)

mod_s_full$Series.residuals

serial.test(mod1, lags.bg = 4, type = "BG")

################ structural Analysis ########################

# creating the A and B matrices for estimation, A is triangular with ones on diagonal
# B is diagonal
# NAs indicate parameters to be estimated
K <- length(var_names) 
A <- diag(K)
B <- diag(K)
for (n in c(1:K)){
  A[n,1:n-1] <- NA
  B[n,n] <- NA}
# add an overidentifying retsriction to the A matrix, excluding cpi from taylor rule
#A[4,1] = 0

triang = A + B
svar1 <- SVAR(mod1, estmethod = "scoring", Amat = A, Bmat = B)
svar1$LR
svar1.irfs <- irf(mod1, impulse = c("l_dm2m"), type = "multiple", n.ahead = 48, ci=0.95)
plotirfs(svar1.irfs)



