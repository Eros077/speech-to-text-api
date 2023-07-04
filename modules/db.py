import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import datetime

directorio_actual = os.path.dirname(os.path.abspath(__file__))
path_to_json = os.path.join(
    directorio_actual,
    "json_keys/your_firebase_key.json",
)

# Initialize the Firebase Admin SDK
cred = credentials.Certificate(path_to_json)
firebase_admin.initialize_app(cred)

# Get a Firestore client(una instancia)
db = firestore.client()


def find_index(array, condition):
    index = next((i for i, elem in enumerate(array) if condition(elem)), None)
    return index


def elderlyExists(elderlyId):
    elderly_ref = db.collection("elderlyUsers").document(elderlyId)
    elderly = elderly_ref.get().to_dict()
    return elderly != None


# Crea una interview y la deja como processing
def createInterview(elderlyId, audio_url):
    status = "processing"
    dateCreated = datetime.datetime.now()

    elderly_ref = db.collection("elderlyUsers").document(elderlyId)
    elderly = elderly_ref.get().to_dict()

    residence_ref = db.collection("residences").document(elderly["residenceId"])

    data = {
        "textOriginal": None,
        "textProcessed": None,
        "brief": None,
        "audioUrl": audio_url,
        "elderly": {
            "id": elderlyId,
            "name": elderly["name"],
            "lastname": elderly["lastname"],
        },
        "residenceId": elderly["residenceId"],
        "dateCreated": dateCreated,
        "status": status,
    }
    interviews_ref = db.collection("interviews")
    _, interview_ref = interviews_ref.add(data)

    # Duplicamos información en el array de interviews de elderly
    elderly_ref.update(
        {
            "interviews": firestore.ArrayUnion(
                [
                    {
                        "id": interview_ref.id,
                        "brief": None,
                        "dateCreated": dateCreated,
                        "residenceId": elderly["residenceId"],
                        "status": status,
                    }
                ]
            )
        }
    )

    # Duplicamos información en el array de interviews de residence
    residence_ref.update(
        {
            "interviews": firestore.ArrayUnion(
                [
                    {
                        "id": interview_ref.id,
                        "brief": None,
                        "dateCreated": dateCreated,
                        "elderlyId": elderlyId,
                        "status": status,
                    }
                ]
            )
        }
    )

    return interview_ref.id


def updateInterview(
    interview_id, status, texto_original, texto_procesado, brief, camposExtraidos={}
):
    interview_ref = db.collection("interviews").document(interview_id)
    interview = interview_ref.get().to_dict()

    data = {
        "textOriginal": texto_original,
        "textProcessed": texto_procesado,
        "brief": brief,
        "status": status,
        "camposExtraidos": camposExtraidos,
    }
    interview_ref.update(data)

    transaction = db.transaction()

    @firestore.transactional
    def update_in_transaction(transaction):
        # Actualizar brief en el array de interviews del elderly
        elderly_ref = db.collection("elderlyUsers").document(interview["elderly"]["id"])
        elderly = elderly_ref.get().to_dict()
        interview_index = find_index(
            elderly["interviews"], lambda interview: interview["id"] == interview_id
        )
        elderly["interviews"][interview_index]["brief"] = brief
        elderly["interviews"][interview_index]["status"] = status
        transaction.update(elderly_ref, {"interviews": elderly["interviews"]})

        # Actualizar brief en el array de interviews del residence
        residence_ref = db.collection("residences").document(interview["residenceId"])
        residence = residence_ref.get().to_dict()
        interview_index = find_index(
            residence["interviews"], lambda interview: interview["id"] == interview_id
        )
        residence["interviews"][interview_index]["brief"] = brief
        residence["interviews"][interview_index]["status"] = status
        transaction.update(residence_ref, {"interviews": residence["interviews"]})

    update_in_transaction(transaction)
