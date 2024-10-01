import zmq

def validate_input(input_string):
    # validate the input based on requirements
    if len(input_string) != 5:
        return False
    code, char = input_string.split("_")
    if not (code.isdigit() and len(code) == 3 and char in ['a', 'b', 'c']):
        return False
    return True

def microservice():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")  # listening on port 5555

    while True:
        # wait for next request from client
        request = socket.recv_string()
        print(f"Received request: {request}")

        # validate request
        if validate_input(request):
            # process request
            code, char = request.split("_")
            if code not in codes_seen:
                codes_seen.add(code)
                response = "valid"
            else:
                response = "invalid"
        else:
            response = "invalid"

        # send reply back to client
        socket.send_string(response)

    socket.close()
    context.term()

if __name__ == "__main__":
    codes_seen = set()    # store unqiue ids
    microservice()
