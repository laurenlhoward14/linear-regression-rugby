def split_data(dataframe, y_column):
    ''' Takes in dataframe and splits into 80% training and 20% testing data'''

    X, y = dataframe.drop(y_column, axis=1), dataframe[y_column]
    X_train, X_hold_out, y_train, y_hold_out = train_test_split(X, y, test_size=.2, random_state=27) # 80% Train 20% Test
    kf = KFold(n_splits=5, shuffle=True, random_state = 27)


def reg_plot(x, y):
    ''' Takes in all of the X values and Y predictor '''

    plt.figure(figsize=(15, 5))

    lr = LinearRegression()
    lr.fit(x,y)
    pred = lr.predict(x)

    # Residual plot
    plt.subplot(1, 2, 1)
    res = y - pred
    plt.scatter(pred, res)
    plt.title("Residual plot")
    plt.xlabel("prediction")
    plt.ylabel("residuals")

    # QQ plot
    plt.subplot(1, 2, 2)
    stats.probplot(res, dist="norm", plot=plt)
    plt.title("Normal Q-Q plot")


def lin_reg(dataframe, predictor_col):

    """Performs linear regression - takes in a dataframe and its predictor column"""

    X, y = dataframe.drop(predictor_col, axis=1), dataframe[predictor_col]

    X, X_test, y, y_test = train_test_split(X, y, test_size=.2, random_state=27)
    X, y = np.array(X), np.array(y)

    kf = KFold(n_splits=5, shuffle=True, random_state = 27)
    cv_val_r2 = []
    train_r2 = []

    for train, val in kf.split(X, y):

        X_train, y_train = X[train], y[train]
        X_val, y_val = X[val], y[val]

        lm = LinearRegression()
        lm.fit(X_train, y_train)
        train_r2.append(lm.score(X_train, y_train))
        cv_val_r2.append(lm.score(X_val, y_val))


    print(f"Mean of Train Scores: {np.mean(train_r2):.3f}")
    print(f"Mean of Linear Regression Scores: {np.mean(cv_val_r2):.3f}")



def ridge_reg(X, y, columns):

    """Performs Ridge Regression using multiple values of alpha and locates optimal alpha"""

    X, y = np.array(X), np.array(y)

    alpha_list = [0.001, 0.01, 0.1,1,10,100,1000,10000,100000, 1000000]
    ridge_train_r2 = []
    ridge_val_r2 = []
    differences = []
    ridge_means = []

    for alp in alpha_list:
        for train, val in kf.split(X, y):

            X_train, y_train = X[train], y[train]
            X_val, y_val = X[val], y[val]

            lm_reg = Ridge(alpha=alp)

            # Ridge Scale
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_val_scaled = scaler.transform(X_val)

            lm_reg.fit(X_train_scaled, y_train)
            ridge_train_r2.append(lm_reg.score(X_train_scaled, y_train))
            ridge_val_r2.append(lm_reg.score(X_val_scaled, y_val))

            difference = np.mean(ridge_train_r2) - np.mean(ridge_val_r2)

        ridge_means.append(np.mean(ridge_val_r2))
        best_mean = max(ridge_means)

    max_in = 0
    max_mean = 0
    for i, l in enumerate(ridge_means):
        if l > max_mean:
            max_mean = l
            max_in = i
    best_alpha = alpha_list[max_in]
    print(f"Best Alpha: {best_alpha}")

    ridge_model = Ridge(alpha=best_alpha)
    ridge_model.fit(X_train_scaled, y_train)
    train_r2 = ridge_model.score(X_train_scaled, y_train)
    val_r2 = ridge_model.score(X_val_scaled, y_val)

    print(f"Train r2: {train_r2}")
    print(f"Val r2: {val_r2}\n")
    print(list(zip(columns, ridge_model.coef_)))


def lasso_reg(X, y, columns):

    """Performs Ridge Regression using multiple values of alpha and locates optimal alpha"""

    X, y = np.array(X), np.array(y)

    alpha_list = [0.001, 0.01, 0.1,1,10,100,1000,10000,100000, 1000000]
    lasso_train_r2 = []
    lasso_val_r2 = []
    differences = []
    lasso_means = []

    for i, alp in enumerate(alpha_list):
        for train, val in kf.split(X, y):

            X_train, y_train = X[train], y[train] # Split training into train and val
            X_val, y_val = X[val], y[val]

            lm_lasso = Lasso(alpha=alp)

            #Lasso Scale
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_val_scaled = scaler.transform(X_val)

            lm_lasso.fit(X_train_scaled, y_train)

            lasso_train_r2.append(lm_lasso.score(X_train_scaled, y_train))
            lasso_val_r2.append(lm_lasso.score(X_val_scaled, y_val))

            difference = np.mean(lasso_train_r2)- np.mean(lasso_val_r2)

        lasso_means.append(np.mean(lasso_val_r2))
        best_mean = max(lasso_means)

    max_in = 0
    max_mean = 0
    for i, l in enumerate(lasso_means):
        if l > max_mean:
            max_mean = l
            max_in = i
    best_alpha = alpha_list[max_in]
    print(f"Best Alpha: {best_alpha}\n")

    lasso_model = Lasso(alpha=best_alpha)
    lasso_model.fit(X_train_scaled, y_train)
    train_r2 = lasso_model.score(X_train_scaled, y_train)
    val_r2 = lasso_model.score(X_val_scaled, y_val)

    print(f"Train r2: {train_r2}")
    print(f"Val r2: {val_r2}\n")
    print(list(zip(columns, lasso_model.coef_)))
