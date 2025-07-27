from circular_chart import CircularChart

def main():
    print("Hello from knitting-pi!")
    chart = CircularChart(4,4)
    chart.generate_random_chart()
    chart.print_chart_2()

if __name__ == "__main__":
    main()