from utils import get_data
from graphs import generate_graphs
from app import app

def main()->None:
    data = get_data()
    generate_graphs(data)
    app.run(host='localhost',debug=True)

if __name__=='__main__':
    main()