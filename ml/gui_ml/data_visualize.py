import pandas as pd



class data_:

    def read_file(self, filepath):
        if str(filepath) == "":
            return ""
        
        else :
            return pd.read_csv(str(filepath), index_col=False)
    
    def get_column_list(self, df):
        # print(list(df.columns))
        # columnname_list = []
        # for i in df.columns:
        #     columnname_list.append(i)
        return  list(df.columns)