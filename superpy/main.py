# Imports
import argparse
import csv
from rich import print
from rich.table import Table
from datetime import datetime, timedelta
from pathlib import Path
import plotly.graph_objects as px
from pandas import read_csv
from src.report import Report

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'


# Your code below this line.

# Date written to file.
internal_date = datetime.now().date()
# Actual current OS date.
current_date = datetime.now().date()
report = Report('sold.csv','bought.csv')

def main():
    global internal_date
    parser = argparse.ArgumentParser(description = 'Process some integers.')
    # parser.add_argument('type', type = str, help = 'Type of action, must be either buy, sell, report or advance.')
    subparsers = parser.add_subparsers(title = 'subcommands', description = 'valid subcommands', help = 'additional help', dest = 'type')
 
    # Command Buy
    parser_buy = subparsers.add_parser('buy',  help = 'Command for when you want to register a product as bought.')   
    parser_buy.add_argument('--product-name', type = str, help = 'Name of a product the supermarket offers.')
    parser_buy.add_argument('--price', type = float, help = 'The amount of money per product the supermarket paid for it.')
    parser_buy.add_argument('--expiration-date', type = str, help = 'The date on which the product the supermarket has in stock expires. The date shows the year first, than the month and lastly the day.')

    # Command Sell
    parser_sell = subparsers.add_parser('sell', help = 'Command for when you want to register a product as sold.')
    parser_sell.add_argument('--bought-id', type = int, help = 'Id of the sold product as it is declared in the bought.csv file.')
    parser_sell.add_argument('--price', type = float, help = 'The amount of money per product the supermarket sold it for.')
    
    # Command Advance
    parser_advance = subparsers.add_parser('advance', help = 'Command for when you want to forward the internal time.')
    parser_advance.add_argument('--advance-time', default = 0, type = int, help = 'A tool which you can use to fastworward the time to two days later.')
    
    # Command Report
    parser_report = subparsers.add_parser('report', help = 'Command for when you want to generate a report.')
    parser_report_type = parser_report.add_subparsers(title = 'reports', description = 'report types', help = 'additional help', dest = 'report_type')
    parser_inventory = parser_report_type.add_parser('inventory', help = 'Reports the inventory of a specified date.')   
    parser_revenue = parser_report_type.add_parser('revenue', help = 'Reports the revenue of a specified date or period.')   
    parser_profit = parser_report_type.add_parser('profit', help = 'Reports the profit of a specified date or period.')   
    parser_revenue_chart = parser_report_type.add_parser('revenue_chart', help = 'Creates a chart of the revenue.')   

    parser_inventory.add_argument('--tocsv', action = 'store_true', help = 'Export a csv file containing the inventory of the requested date.')
    parser_inventory.add_argument('--date', type = str, help = 'Manner to specify a specific moment in time.')
    parser_inventory.add_argument('--yesterday', action = 'store_true', help = 'Manner to specify a specific moment in time, only used for reports.')
    parser_revenue.add_argument('--date', type = str, help = 'Manner to specify a specific moment in time.')
    parser_revenue.add_argument('--yesterday', action = 'store_true', help = 'Manner to specify a specific moment in time, only used for reports.')
    parser_profit.add_argument('--date', type = str, help = 'Manner to specify a specific moment in time.')
    parser_profit.add_argument('--yesterday', action = 'store_true', help = 'Manner to specify a specific moment in time, only used for reports.')
    internal_date = get_internal_date()
    args = parser.parse_args()

    print(args)

    # To advance time by one day or more.
    if args.type == 'advance' and args.advance_time:
        temp_date = internal_date + timedelta(days=args.advance_time)
        internal_date = set_internal_date(temp_date)
        return print('[green][bold]OK[/green][/bold]')

    
    if args.type == 'buy':
        write_buy_to_csv(args.product_name, args.price, args.expiration_date)
    if args.type == 'sell':
        write_sell_to_csv(args.bought_id, args.price)
    if args.type == 'report':
        period = 'Today'
        check_date = datetime.now().strftime('%Y-%m-%d')
        if args.yesterday:
            period = 'Yesterday'
            check_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        if args.date:
            period = args.date
            check_date = args.date
        if args.report_type == "revenue_chart":
            report.show_revenue_chart()
        if args.report_type == 'revenue':
            report.report_revenue(period, check_date)
        if args.report_type == 'profit':
            report.report_profit(period, check_date)
        if args.report_type == 'inventory':
            report.report_inventory(period, check_date, args.tocsv)    
        

def get_internal_date():
    try:
        f = open('time.txt', 'r')
        file_date = f.read()
        return datetime.strptime(file_date, '%Y-%m-%d').date()
    except FileNotFoundError:
        f = open('time.txt', 'x')
        f.write(datetime.now().date().strftime('%Y-%m-%d'))
        return datetime.now().date()
    finally:
        f.close()

def set_internal_date(new_date:datetime):
    f = open('time.txt', 'w')
    f.write(new_date.strftime('%Y-%m-%d'))
    f.close()
    return new_date
    
# Transfer data bought products to CSV-file.    
def write_buy_to_csv(product_name: str, buy_price: float, expiration_date: str):
    global current_date
    id = 1

    # Checks if exists, if not creates the file.
    Path('bought.csv').touch(exist_ok = True)
    
    write_file = open('bought.csv', 'a+', newline = '')
    read_file = open('bought.csv', 'r', newline = '')

    # Read current Id
    reader = csv.reader(read_file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
    readlist = list(reader)

    # Gives Id-number to bought product.
    if len(readlist) > 0:
        id = int(readlist[len(readlist) - 1][0]) + 1
    read_file.close() 
    writer = csv.writer(write_file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
    if id == 1:
        writer.writerow(["bought_id", "product_name", "buy_date", "buy_price", "expiration_date", "sold_date"])
    
    writer.writerow([id, product_name, current_date.strftime('%Y-%m-%d'), buy_price, expiration_date, None])

    write_file.close() 
    print('[green]Product has been added to the inventory.[/green]')

# Transfer data sold products to CSV-file.
def write_sell_to_csv(bought_id: int, sell_price: float):
    global current_date
    id = 1

    # Declare files.
    Path('bought.csv').touch(exist_ok=True)
    Path('sold.csv').touch(exist_ok=True)
    sold_read_file = open('sold.csv', 'r+', newline = '') 
    bought_read_file = open('bought.csv', 'r+', newline = '') 

    # Read current Id
    reader = csv.reader(sold_read_file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
    readlist = list(reader)

    # Gives Id-number to sold product.
    if len(readlist) > 0:
        id = int(readlist[len(readlist) - 1][0]) + 1
    sold_read_file.close()

    # Get associated bought Id
    bought_reader = csv.reader(bought_read_file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
    bought_list = list(bought_reader)
    product_name = ''

    # Add sold date to item in bought.csv
    for line, row in enumerate(bought_list):
        if row[0] == str(bought_id):
            product_name = row[1]
            bought_list[line][5] = current_date.strftime('%Y-%m-%d')
            break
    bought_read_file.close()
    
    # When bought_id not found
    if product_name == '':
        print('[red]Error: Product not found in the inventory.[red]')
        return
    
    bought_write_file = open('bought.csv', 'w+', newline='') 
    bought_writer = csv.writer(bought_write_file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
    bought_writer.writerows(bought_list)

    bought_write_file.close()

    sold_write_file = open('sold.csv', 'a+', newline='') 

    writer = csv.writer(sold_write_file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
    if id == 1:
        writer.writerow(["sold_id", "bought_id", "product_name", "sold_date", "sell_price"])
    
    writer.writerow([id, bought_id, product_name, current_date.strftime('%Y-%m-%d'), sell_price])  
    sold_write_file.close() 
    print('[green]Product has been removed from the inventory.[/green]')

if __name__ == '__main__':
    main()
