# Report


## Technical element 1:

In my code I used the argument bought_id when you want to add a sold product to the sold.csv file and to remove it from the inventory. I did this to solve two problems; the first problem was that I needed a way to write off the product in the inventory corresponding to the sold product. The only way this could be done was with a corresponding Id-number. If I would have used only the product name it would have written off the first product with that name in the bought.csv, regardless of the expiration date etc. The second problem it solved was that it was less sensitive to wrong product names if I would have chosen that instead of the bought_id. For example; someone could type “oranges” but in the bought.csv it exists as “orange”, then you would get back an error. With the usage of the bought_id this kind of mistakes are less common.

## Technical element 2:

I added a column to the bought.csv with the date on which this specific product was sold. This date is added when the employee (or you) enters a sold product into the command-line. 

``` python
for line, row in enumerate(bought_list):
        if row[0] == str(bought_id):
            product_name = row[1]
            bought_list[line][5] = current_date.strftime('%Y-%m-%d')
            break
    bought_read_file.close()
```

This way you know when something is sold and the employee (or you) will only have to check the bought.csv file to get an inventory report. Otherwise you would have to constantly check the sold.csv file as well to cross-reference it with the bought.csv file to see what is still left in inventory.

## Technical element 3:

I used Pandas to read the CSV-files so that the data is corresponded immediately and correctly to plotly for the chart. This way plotly knows what data to show. 

``` python
data = read_csv(self.sold_csv, header=0, index_col=0, parse_dates=True, squeeze=True)
        print(data)
```

If I didn’t use pandas and tried to open or read the CSV-files it would not recognize the data but with Panda it did. For this I did have to give the CSV-files headers.
