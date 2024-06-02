import random
import string

def generate_room_code(active_sessions: set) -> str:
    """
    Generate a unique 4-letter room code consisting of uppercase letters.

    This function continuously generates a new room code until it finds one
    that is not already in the active_sessions set. If all possible permutations
    of 4-letter codes are exhausted, it returns an error string.

    Args:
        active_sessions (set): A set containing active room codes.

    Returns:
        str: A unique 4-letter room code, or an error string if no unique code
             can be generated.
    """
    # Check if all possible permutations of 4-letter codes are exhausted
    if len(active_sessions) >= 26 ** 4:
        return "ERROR: All possible room codes are in use."

    while True:
        room_code = ''.join(random.sample(string.ascii_uppercase, k=4))
        if room_code not in active_sessions:
            return room_code


@socketio.on('start_session', namespace='/local')
def start_session_app() -> None:
    """
    Handles the 'start_session' event in the '/local' namespace.

    This function generates a unique session ID (room code) and client ID,
    joins the session room, and emits the session ID to the local game.
    If an error occurs during the generation of the room code, it emits
    an error message instead.

    Returns:
        None
    """
    # Generate a unique session ID (room code)
    session_id: str = generate_room_code()
    
    # Get the client ID of the requester
    client_id: str = request.sid

    if "ERROR" in session_id:
        # An error occurred during room code generation
        emit(
            'error_message',
            {'error': room_code_or_error},
            namespace='/local',
            room=client_id
        )
    else:
        # Join the session
        start_session(session_id, client_id, 'local')

        # Emit the session ID (room code) to the local game
        emit(
            'receive_room_code',
            {'session_id': session_id},
            namespace='/local',
            room=client_id
        )
