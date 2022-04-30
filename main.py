from graphs import get_data,generate_graphs

def main()->None:
    data = get_data()
    generate_graphs(data)

if __name__=='__main__':
    main()