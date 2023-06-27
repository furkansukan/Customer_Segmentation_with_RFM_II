###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

# 1. İş Problemi (Business Problem)
# 2. Veriyi Anlama (Data Understanding)
# 3. Veri Hazırlama (Data Preparation)
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
# 7. Tüm Sürecin Fonksiyonlaştırılması

###############################################################
# 1. İş Problemi (Business Problem)
###############################################################

# About Dataset
# Data holds the basic information about sales data.
# The company have sales agencies / resellers and branches and
# the data file holds only the branch/reseller information in the customer field.

# Veri Seti Hikayesi
# https://www.kaggle.com/datasets/shedai/retail-data-set


# Değişkenler
#
# InvoiceID : ID of the transaction. A transaction might hold multiple records for the same customer at the same date with multiple products (SKU). DocumentID might be useful for combining the transactions and detecting the items sold together.
# Date : Date of transaction / sell. In the date time format.
# ProductID : Item / Product code. The unique code for each item sold.
# TotalSales : Sales price for the transaction. If you want to get unit_price , divide TotalSales column to Quantity column
# Discount : Discount amount for the transaction.
# CustomerID : Unique customer id for each customer. For the data set, customer can be a reseller or a branch of the company.
# Quantity : Number of items sold in the transaction.




###############################################################
# 2. Veriyi Anlama (Data Understanding)
###############################################################
import pandas as pd
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

df_ = pd.read_csv("datasets/file_out2.csv")
df = df_.copy()
df.head()

def check_df(dataframe):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(5))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

df.groupby("CustomerID").agg({"InvoiceID": ["count"],
                              "TotalSales": ["mean", "sum"]

})

df.groupby([ "CustomerID", "InvoiceID"]).agg({"Date": ["min", "max"],
                             "Discount": ["max"]

})

df["TotalSales"]
###############################################################
# 3. Veri Hazırlama (Data Preparation)
###############################################################

df.isnull().sum()
df.drop("Unnamed: 0", axis=1, inplace=True)
df.head()
###############################################################
# 4. RFM Metriklerinin Hesaplanması (Calculating RFM Metrics)
###############################################################

# Recency, Frequency, Monetary
df["Date"].max()
# '2023-03-25'

today_date = dt.datetime(2023, 3, 25)
df["Date"] = pd.to_datetime(df["Date"])
rfm = df.groupby("CustomerID").agg({"Date": lambda Date: (today_date - Date.max()).days,
                                    "InvoiceID": lambda InvoiceID: InvoiceID.nunique(),
                                    "TotalSales": lambda TotalSales: TotalSales.sum()
})

rfm.head()

rfm.columns = ["Recency", "Frequency", "Monetary"]
rfm.describe().T

###############################################################
# 5. RFM Skorlarının Hesaplanması (Calculating RFM Scores)
###############################################################

# Recency değeri için 5 skor oluşturulurken, en yüksek değer 5 ve en düşük değer 1 olarak etiketlenir.
# Frequency değeri için, müşterilerin sıralamasına göre 5 skor oluşturulur ve etiketlenir.
# Monetary değeri için de 5 skor oluşturulur ve etiketlenir.


rfm["recency_score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm["Frequency"].rank(method= "first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5])

rfm.head()

rfm["RFM_SCORE"] = rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)
###############################################################
# 6. RFM Segmentlerinin Oluşturulması ve Analiz Edilmesi (Creating & Analysing RFM Segments)
###############################################################
# regex

# RFM isimlendirmesi

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm["segment"] = rfm["RFM_SCORE"].replace(seg_map, regex=True)

new_df = pd.DataFrame()

new_df["new_customer_id"] = rfm[rfm["segment"] == "new_customers"].index

new_df["new_customer_id"] = new_df["new_customer_id"].astype(int)

rfm.to_excel("RFM.xlsx")

rfm.tail(52)

###############################################################
# 7. Tüm Sürecin Fonksiyonlaştırılması
###############################################################


def create_rfm(dataframe, csv=False):

    # VERIYI HAZIRLAMA
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]

    # RFM METRIKLERININ HESAPLANMASI
    today_date = dt.datetime(2011, 12, 11)
    rfm = dataframe.groupby('Customer ID').agg({'InvoiceDate': lambda date: (today_date - date.max()).days,
                                                'Invoice': lambda num: num.nunique(),
                                                "TotalPrice": lambda price: price.sum()})
    rfm.columns = ['recency', 'frequency', "monetary"]
    rfm = rfm[(rfm['monetary'] > 0)]

    # RFM SKORLARININ HESAPLANMASI
    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

    # cltv_df skorları kategorik değere dönüştürülüp df'e eklendi
    rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                        rfm['frequency_score'].astype(str))


    # SEGMENTLERIN ISIMLENDIRILMESI
    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

    rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)
    rfm = rfm[["recency", "frequency", "monetary", "segment"]]
    rfm.index = rfm.index.astype(int)

    if csv:
        rfm.to_csv("rfm.csv")

    return rfm

df = df_.copy()

rfm_new = create_rfm(df, csv=False)










