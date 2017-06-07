# Suppose data is loaded. 
require(xgboost)
library(xgboost)



train$label = Final_data_v1$mortality
train$data = subset(Final_data_v1,select=NMBA:PaO2.FIO2)
dim(train$data)
N = dim(train$data)[1]
N_do1 = 77 
N_do0 = N-77

test$data = matrix(0, ncol = 11, nrow = N*N )
test$label = rep(0,N*N)
test_idx = 0 
for (i in 1:N){
  # print ((i/N)*100)
  for (k in 1:N){
    test_idx = test_idx + 1 
    # print (c(i,k))
    test$data[test_idx,] = c(train$data[i,1], as.matrix(train$data[k,])[-1])
    test$label[test_idx] = train$label[i]
  }
}

bst <- xgboost(data = as.matrix(train$data), label = train$label, max.depth = 10, eta = 1, nthread = 2, nround = 10, objective = "binary:logistic")
pred = predict(bst,as.matrix(test$data))

N_pred = length(pred)
pred_indiv = rep(0,N)

for (i in 1:N){
  pred_sum = 0
  for (k in i:N){
    pred_sum = pred_sum + pred[(i-1)*N + k]  
  }
  pred_indiv[i] = pred_sum / N
}

print (c( mean(pred_indiv[1:77]), mean(pred_indiv[78:308])  ))



