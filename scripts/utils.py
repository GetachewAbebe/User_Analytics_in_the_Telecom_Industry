
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from typing import Optional


class Util:

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def count_outliers(self, Q1, Q3, IQR, columns):
        cut_off = IQR * 1.5
        temp_df = (self.df[columns] < (Q1 - cut_off)) | (self.df[columns] > (Q3 + cut_off))
        return [len(temp_df[temp_df[col] == True]) for col in temp_df]

    def calc_skew(self, columns=None):
        if columns == None:
            columns = self.df.columns
        return [self.df[col].skew() for col in columns]

    def percentage(self, list):
        return [str(round(((value/150001) * 100), 2)) + '%' for value in list]

    def remove_outliers(self, columns):
        for col in columns:
            Q1, Q3 = self.df[col].quantile(0.25), self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            cut_off = IQR * 1.5
            lower, upper = Q1 - cut_off, Q3 + cut_off
            self.df = self.df.drop(self.df[self.df[col] > upper].index)
            self.df = self.df.drop(self.df[self.df[col] < lower].index)

    def replace_outliers_with_fences(self, columns):
        for col in columns:
            Q1, Q3 = self.df[col].quantile(0.25), self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            cut_off = IQR * 1.5
            lower, upper = Q1 - cut_off, Q3 + cut_off

            self.df[col] = np.where(self.df[col] > upper, upper, self.df[col])
            self.df[col] = np.where(self.df[col] < lower, lower, self.df[col])

    def getOverview(self, columns) -> Optional[pd.DataFrame]:
        min = self.df[columns].min()
        Q1 = self.df[columns].quantile(0.25)
        median = self.df[columns].quantile(0.5)
        Q3 = self.df[columns].quantile(0.75)
        max = self.df[columns].max()
        IQR = Q3 - Q1
        skew = self.calc_skew(columns)
        outliers = self.count_outliers(Q1, Q3, IQR, columns)
        cut_off = IQR * 1.5
        lower, upper = Q1 - cut_off, Q3 + cut_off

        new_columns = [
            'Name of columns',
            'Min',
            'Q1',
            'Median',
            'Q3',
            'Max',
            'IQR',
            'Lower fence',
            'Upper fence',
            'Skew',
            'Number_of_outliers',
            'Percentage_of_outliers' ]
        data = zip(
            [column for column in self.df[columns]],
            min,
            Q1,
            median,
            Q3,
            max,
            IQR,
            lower,
            upper,
            skew,
            outliers,
            self.percentage(outliers)
        )
        new_df = pd.DataFrame(data=data, columns=new_columns)
        new_df.set_index('Name of columns', inplace=True)
        return new_df.sort_values('Number_of_outliers', ascending=False).transpose()
    
    def count_values(self, df, column):
        new_df = df[column].value_counts().reset_index()
        new_df = new_df.rename(
            columns={'index': column, column: "count"})
        return new_df

    def find_agg(self, df: pd.DataFrame, agg_column: str, agg_metric: str, col_name: str, order=False) -> pd.DataFrame:
        new_df = df.groupby(agg_column)[agg_column].agg(agg_metric).reset_index(name=col_name).sort_values(by=col_name,
            ascending=order)
        return new_df.reset_index(drop=True)
    
    def choose_kmeans(self, df: pd.DataFrame, num: int):
        #Distortion is the average of the euclidean squared distance from the centroid of their respective clusters.
        # Inertia is the sum of squared distances of samples to their closest cluster centre.
        distortions = []
        inertias = []
        K = range(1, num)
        for k in K:
            kmeans = KMeans(n_clusters=k, random_state=0).fit(df)
            distortions.append(sum(
                np.min(cdist(df, kmeans.cluster_centers_, 'euclidean'), axis=1)) / df.shape[0])
            inertias.append(kmeans.inertia_)

        return (distortions, inertias)
