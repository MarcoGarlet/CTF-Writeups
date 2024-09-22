from flask import Flask, request
import uuid, subprocess


app = Flask(__name__)
SECRET = open("/app/secret.txt", "r").read()
stats = []

@app.route('/', methods=['GET'])
def main():
    print('HELLO FROM PRINT', flush=True)
    return 'Hello, World!'

@app.route('/api/stats/<string:id>', methods=['GET'])
def get_stats(id):
    print(f'Dentro la rotta GET api stats: {id}', flush=True)
    for stat in stats:
        if stat['id'] == id:
            return str(stat['data'])
        
    return '{"error": "Not found"}'

@app.route('/api/stats', methods=['POST'])
def add_stats():
    try:
        username = request.json['username']
        high_score = int(request.json['high_score'])
    except:
        return '{"error": "Invalid request"}'
    
    id = str(uuid.uuid4())

    stats.append({
        'id': id,
        'data': [username, high_score]
    })
    return '{"success": "Added", "id": "'+id+'"}'

@app.route('/api/cal', methods=['GET'])
def get_cal():
    cookie = request.cookies.get('secret')
    print(f'Finalmente dentro cal {cookie} => {cookie == SECRET}',flush=True)
    if cookie == None:
        return '{"error": "Unauthorized"}'
    
    if cookie != SECRET:
        return '{"error": "Unauthorized"}'
    
    modifier = request.args.get('modifier','')
    print(f'=> Modifier = {modifier}',flush=True)
    print(f'output of subprocess = ${subprocess.getoutput("cal "+modifier)}',flush=True)
    return '{"cal": "'+subprocess.getoutput("cal "+modifier)+'"}'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337, threaded=True)