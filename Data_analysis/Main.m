Y = Data(:,2);
X = Data(:,3);
Z = Data(:,4:13);
X_aug = [X,Z];
b = glmfit(X_aug,Y,'binomial','link','logit');
N = length(Data);
P_val = zeros(1,2); P_val_idx = 1;
p_val = 0;
for i = 1:N,
    glmval_sum = 0;
    for k = 1:N
        x_aug = [X(i), Z(k,:)];
        glmval_sum = glmval_sum + glmval(b,x_aug,'logit');
    end
    glm_final = glmval_sum / N;
    if p_val ~= glm_final
        P_val(P_val_idx) = glm_final;
        p_val = glm_final;
        P_val_idx = P_val_idx + 1;
    end
end