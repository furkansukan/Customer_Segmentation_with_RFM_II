# Customer_Segmentation_with_RFM_II
RFM ile Müşteri Segmentasyonu 2

Business Problem

![image](https://github.com/furkansukan/Customer_Segmentation_with_RFM_II/assets/115731123/e3b2410f-2373-4968-9908-78b5ee0c7ad7)


About Dataset
Data holds the basic information about sales data.
The company have sales agencies / resellers and branches and the data file holds only the branch/reseller information in the customer field.

# Veri Seti Hikayesi
https://www.kaggle.com/datasets/shedai/retail-data-set


# Değişkenler

InvoiceID : ID of the transaction. A transaction might hold multiple records for the same customer at the same date with multiple products (SKU). DocumentID might be useful for combining the transactions and detecting the items sold together.

Date : Date of transaction / sell. In the date time format.

ProductID : Item / Product code. The unique code for each item sold.

TotalSales : Sales price for the transaction. If you want to get unit_price , divide TotalSales column to Quantity column

Discount : Discount amount for the transaction.

CustomerID : Unique customer id for each customer. For the data set, customer can be a reseller or a branch of the company.

Quantity : Number of items sold in the transaction.


