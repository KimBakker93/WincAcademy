from rich import print
from rich.table import Table
from datetime import datetime, timedelta
from pathlib import Path
import plotly.graph_objects as px
from pandas import read_csv
import csv

class Report:
    bought_csv = ''
    sold_csv = ''

    def __init__ (self,sold_csv,bought_csv):
        self.sold_csv = sold_csv
        self.bought_csv = bought_csv
    
    # Reports revenue of moment or span of time.
    def report_revenue(self, date_str:str, check_date:str):
        sold_read_file = open(self.sold_csv, 'r+', newline = '')

        # Read current Id
        reader = csv.reader(sold_read_file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        sold_list = list(reader)
        
        # Adding sellprices.
        revenue = 0
        for line, row in enumerate(sold_list):
            if row[3].startswith(check_date):
                revenue += float(row[4])
        print(date_str + "'s revenue is: [green][bold]" + str(round(revenue,2)) + "[/green][/bold]")        

    # Reports profit of certain date. 
    def report_profit(self, date_str:str, check_date_str:str):
        sold_read_file = open(self.sold_csv, 'r+', newline = '')
        bought_read_file = open(self.bought_csv, 'r+', newline = '') 

        # Read current Id
        reader = csv.reader(sold_read_file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        bought_reader = csv.reader(bought_read_file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        sold_list = list(reader)
        
        # Amount sold minus amount bought.
        profit = 0
        for line, row in enumerate(sold_list):
            if row[3].startswith(check_date_str):
                for bought_row in bought_reader:
                    if bought_row[0] == row[1]:
                        profit -= float(bought_row[3])
                profit += float(row[4])
        print(date_str + "'s profit is: [green][bold]" + str(round(profit,2)) + "[/green][/bold]")  
        sold_read_file.close()
        bought_read_file.close()      

    # Reports inventory of certain date.
    def report_inventory(self, date_str:str, check_date_str:str, tocsv:bool):

        # Table lay-out.
        table = Table(title = "Inventory " + check_date_str)
        table.add_column("Id", style = "yellow")
        table.add_column("Product Name", style = "blue")
        table.add_column("Buy Date", style = "white")
        table.add_column("Buy Price", style = "red")
        table.add_column("Expiration Date", style = "green")
        bought_read_file = open(self.bought_csv, 'r+', newline = '')

        # Read current Id
        reader = csv.reader(bought_read_file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        bought_list = list(reader)
        rows = []
        # Bought products minus sold items.
        check_date = datetime.strptime(check_date_str, '%Y-%m-%d')
        for line, row in enumerate(bought_list):
            if line == 0:
                continue
            expire_date = datetime.strptime(row[4], '%Y-%m-%d')
            buy_date = datetime.strptime(row[2], '%Y-%m-%d')
            if row[5] != '':
                sold_date = datetime.strptime(row[5], '%Y-%m-%d')
                if check_date > sold_date:
                    continue
            
        # Exclude expired products from inventory.        
            if check_date < expire_date and check_date >= buy_date:
                rows.append([row[0], row[1], row[2], row[3], row[4]])
                table.add_row(row[0], row[1], row[2], row[3], row[4])
        print(table)  

        # Exports inventory to csv file.
        if tocsv:
            write_file = open('inventory_' + check_date_str + '.csv', 'w+', newline = '')
            writer = csv.writer(write_file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
            writer.writerow(["Id", "Product Name", "Buy Date", "Buy Price", "Expiration Date"])
            writer.writerows(rows)
            write_file.close()
            print('[green]Export [blue]"inventory_' + check_date_str + '.csv"[/blue] created.[/green]')

    # Chart revenue.
    def show_revenue_chart(self):
        data = read_csv(self.sold_csv, header = 0, index_col = 0, parse_dates = True, squeeze = True)
        fig = px.Figure(px.Bar(x = data['sold_date'], y = data['sell_price']))
        fig.update_layout(title="Revenue", xaxis_tickformat = '%Y-%m-%d')
        # fig = px.bar(data, x = "sold_date", y = "sell_price", title = "Revenue", xaxis_tickformat = '%Y-%m-%d')
        fig.show()
        print('[blue]Opening chart in browser.[/blue]')
