# Suppose data is loaded. 
require(xgboost)
library(xgboost)
Final_data_v1 <- read.csv("Data/Final_data_v1.csv")

data(agaricus.train, package='xgboost')
data(agaricus.test, package='xgboost')
train <- agaricus.train

# Preparation of data 
train$label = Final_data_v1$mortality
train$data = subset(Final_data_v1,select=NMBA:PaO2.FIO2)
N = dim(train$data)[1]

# Divide data 
set.seed(123456)
smp_size = floor(0.8 * nrow(train$data))
train_ind = sample(seq_len(nrow(train$data)), size = smp_size)
train_data = train$data[train_ind, ]
train_label = train$label[train_ind]

test_data_GT = train$data[-train_ind, ]
test_label_GT = train$label[-train_ind]

N_col = 11
N = nrow(test_data_GT)

test_data = matrix(0, ncol = N_col, nrow = N*N )
test_label = rep(0,N*N)
test_idx = 0 
for (i in 1:N){
  # print ((i/N)*100)
  for (k in 1:N){
    test_idx = test_idx + 1 
    test_data[test_idx,] = c(test_data_GT[i,1],as.matrix(test_data_GT[k,])[-1])
    test_label[test_idx] = test_label_GT[i]
  }
}

bst <- xgboost(data = as.matrix(train_data), label = train_label, max.depth = 3, eta = 5, nthread = 10, nround = 100, objective = "binary:logistic")
pred = predict(bst,as.matrix(test_data))

N_pred = length(pred)

pred_indiv = rep(0,N)
for (i in 1:N){
  pred_sum = 0
  for (k in i:N){
    pred_sum = pred_sum + pred[(i-1)*N + k]  
  }
  pred_indiv[i] = pred_sum / N
}

for (i in 1:N){
  print(c(pred_indiv[i], test_data_GT[i,1],test_label_GT[i] ))
}



