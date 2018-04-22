# A method that returns the information for all notes passed in
def notes_info(notes):
    notes_list = []

    for note in notes:
        data = {
            'id'   : note.id,
            'text' : note.text
        }

        notes_list.append(data)

    return notes_list