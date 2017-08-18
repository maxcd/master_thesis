
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

#######################################################
############ full smaple analysis#####################
#######################################################

lags <- VARselect(s_full, lag.max = 24)$selection[1]
mod_s_full <- VAR(s_full, p = 9, type = "const")
Sig <- mod_s_full$obs
summary(mod_s_full)

mod_s_full$Series.residuals

# testing for serial correlation 

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
p_vals <- lm_row(mod_s_full, H_max=1, type = "PT.adjusted")
p_vals

serial.test(mod_s_full, lags.bg = 4, type = "ES")

# some stability tests
mod_s_full.reccusum <- stability(mod_s_full, type = "OLS-CUSUM")
names(mod_s_full.reccusum)
mod_s_full.reccusum

reccusum <- stability(mod_s_full, type = "Score-CUSUM")
plot(reccusum)

fluc <-  stability(mod_s_full, type = "fluctuation")
plot(fluc)

################ structural Analysis ########################

 # creating the A and B matrices for estimation, A is triangular with ones on diagonal
 # B is diagonal
 # NAs indicate parameters to be estimated
A <- diag(5)
B <- diag(5)
for (n in c(1:5)){
  A[n,1:n-1] <- NA
  B[n,n] <- NA}
 # add an overidentifying retsriction to the A matrix, excluding cpi from taylor rule

triang = A + B

A[5, 1:4] <- c(0, 0, 0, 0)
A[2,1] <- 0
svar_full <- SVAR(mod_s_full, estmethod = "direct", Bmat = triang)
svar_full$LR

svar_full$A
svar_full$B

Sig_est <- svar_full$Sigma.U

 # test restriction
T = mod_s_full$obs
TLM <- T * log(det(Sig_est)) - log(det())

#######################################################
############    trivariate VAR    #####################  
############ full smaple analysis #####################
#######################################################

lags <- VARselect(s_tri, lag.max = 24)$selection[1]
mod_s_tri <- VAR(s_tri, p = lags, type = "const")
nobs <- mod_s_tri$obs
summary(mod_s_tri)

e <- residuals(mod_s_tri)
beta <- coefficients(mod_s_tri)
ncoeffs <- dim(beta$Series.1)[1]
df <- summary(mod_s_tri$varresult[[1]])$df[2]
# retrieve estimate of the residual Covariance matrix
Cov_e = t(e) %*% e
Cov_e = Cov_e / (nobs - ncoeffs)

# testing for serial correlation 

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
p_vals <- lm_row(mod_stri, H_max=1, type = "PT.adjusted")
p_vals

serial.test(mod_s_tri, lags.bg = 4, type = "ES")

# some stability tests
mod_s_tri.reccusum <- stability(mod_s_tri, type = "OLS-CUSUM")
names(mod_s_tri.reccusum)
mod_s_tri.reccusum

reccusum <- stability(mod_stri, type = "Score-CUSUM")
plot(reccusum)

fluc <-  stability(mod_s_tri, type = "fluctuation")
plot(fluc)

################ structural Analysis ########################

# creating the A and B matrices for estimation, A is triangular with ones on diagonal
# B is diagonal
# NAs indicate parameters to be estimated
A <- diag(3)
B <- diag(3)
for (n in c(1:3)){
  A[n,1:n-1] <- NA
  B[n,n] <- NA}
# add an overidentifying retsriction to the A matrix, excluding cpi from taylor rule

triang = A + B

#A[5, 1:4] <- c(0, 0, 0, 0)
#A[2,1] <- 0
svar_tri <- SVAR(mod_s_tri, estmethod = "direct", Bmat = triang, hessian=TRUE)
svar_tri$LR

# compare the estimmated triangular B matrix to th cholesky decomposition
svar_tri$B
matrix(svar_tri$B, 3, 3)
t(chol(Cov_e))

Sig_est <- svar_tri$Sigma.U

#######################################################
#evaluate tht loglikelihood function to check the python function
#######################################################
Amat <- svar_tri$A
Bmat <- svar_tri$B
sigma <- Cov_e

K <- mod_s_tri$K
obs<- mod_s_tri$obs

logLc <- -1* (-1 * (K * obs/2) * log(2 * pi) + obs/2 *
  log(det(Amat)^2) - obs/2 * log(det(Bmat)^2) -
  obs/2 * sum(diag(t(Amat) %*% solve(t(Bmat)) %*%
                     solve(Bmat) %*% Amat %*% sigma)))


# test restriction
T = mod_s_tri$obs
TLM <- T * log(det(Sig_est)) - log(det())

  ####################################################
  ############ pre 2004 analysis #####################
  ####################################################

VARselect(s_pre, lag.max = 18)$selection
mod_pre <- VAR(s_pre, p = 4, type = "const")
T_pre <- mod_s_full$obs
summary(mod_s_full)

K_max = 15
acorr_free <- c(rep(0,K_max))
for (k in c(1:K_max)){
  mod_pre <- VAR(s_pre, p = k, type = "const")
  acorr <- lm_row(mod_pre, H_max=15, type = "BG") 
  acorr_free[k] <- sum(acorr <= 0.05)
  }
 # return the first autokcorrelation free lag order
lags = match(0, acorr_free) 

mod_pre <- VAR(s_full, p = 4, type = "const")
