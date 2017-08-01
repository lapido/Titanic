def prepareData(data, cabin=False):
    import numpy as np
    import pandas as pd

    #function for separating initials
#     def sepInitials(name):
#         return name.split(',')[1].split('.')[0].strip()
#     df_initials = pd.DataFrame({'Salutation':data['Name'].apply(sepInitials)})
#     df_initials = pd.DataFrame({'Salutation':data['Name'].apply(lambda x: x.split(',')[1].split('.')[0].strip())})
    data = pd.merge(data, pd.DataFrame({'Salutation':data['Name'].apply(lambda x: x.split(',')[1].split('.')[0].strip())}), left_index=True, right_index=True)


    def group_salutation(sa):
        if sa == 'Mr':
            return 'Mr'
        elif sa== 'Mrs':
            return 'Mrs'
        elif sa== 'Miss':
            return 'Miss'
        elif sa=='Master':
            return 'Master'
        else:
            return 'others'
    df_3 = pd.DataFrame({'g_salutation': data['Salutation'].apply(group_salutation)})
    data = pd.merge(data, df_3, left_index=True, right_index=True)

    table = data.pivot_table(values='Age', index=['g_salutation'], columns=['Pclass', 'Sex'], aggfunc=np.median)
    
    def fage(x):
        return table[x['Pclass']][x['Sex']][x['g_salutation']]
    data['Age'].fillna(data[data['Age'].isnull()].apply(fage, axis=1), inplace=True)

    data.drop('Name', axis=1, inplace=True)
    title_dumies = pd.get_dummies(data['g_salutation'], prefix='g_salutation')
    data = pd.concat([data, title_dumies], axis=1)
    data.drop('g_salutation', axis=1, inplace=True)


    data.Embarked.fillna(data.Embarked.max(), inplace=True)
    embarked_dummies = pd.get_dummies(data['Embarked'], prefix='Embarked')
    data = pd.concat([data, embarked_dummies], axis=1)
    data.drop('Embarked', axis=1, inplace=True)


    #processing gender
    data['Sex'] = data['Sex'].map({'male':1, 'female':0})



    #encoding and cleaning cabin
    data.Cabin.fillna('U', inplace=True)
    #mapping each cabin value with the cabin letter
    data['Cabin'] = data['Cabin'].map(lambda c:c[0])
    cabin_dummies = pd.get_dummies(data['Cabin'], prefix='Cabin')
    data = pd.concat([data, cabin_dummies], axis=1)
    data.drop('Cabin', axis=1, inplace=True)


    pclass_dummies = pd.get_dummies(data['Pclass'], prefix='Pclass')
    data = pd.concat([data, pclass_dummies], axis=1)
    data.drop('Pclass', axis=1, inplace=True)

    #creating a new feature called family size
    data['FamilySize'] = data['Parch'] + data['SibSp'] +1 
    data['Singleton'] = data['FamilySize'].map(lambda s: 1 if s == 1 else 0)
    data['SmallFamily'] = data['FamilySize'].map(lambda s: 1 if 2<=s<=4 else 0)
    data['LargeFamily'] = data['FamilySize'].map(lambda s: 1 if 5<=s else 0)

    data.drop(['Salutation','Ticket'], axis=1, inplace=True)
    if cabin:
        data.drop(['Cabin_T'], axis=1, inplace=True)

    if (data.Age.isnull().sum() > 0):
        data_test.Age.fillna(data_test.Age.median(), inplace=True)
    if (data.Fare.isnull().sum() > 0):
        data_test.Fare.fillna(data_test.Fare.median(), inplace=True)


    return data

