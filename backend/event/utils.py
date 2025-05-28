# event/utils.py
import hashlib
import json
from decimal import Decimal

# Importe seus modelos de evento específico se necessário para obter mais detalhes
from .models import Event # , Movement, Weighing, Vacine, Medicine, Reproduction, Slaughter, SpecialOccurrences

def generate_event_data_hash(event_instance):
    """
    Gera um hash SHA256 para os dados relevantes de uma instância de Evento
    e seus detalhes específicos, se houver.
    """
    data_to_hash = {
        "event_id_db": event_instance.id, # ID do evento no banco de dados Django
        "animal_id_db": event_instance.animal.id,
        "event_type_id_db": event_instance.event_type.id,
        "event_type_name": event_instance.event_type.name, # Nome do tipo de evento
        "date": event_instance.date.isoformat(),
        "location": event_instance.location,
        "observations": event_instance.observations,
        "recorded_by_user_id_db": event_instance.recorded_by.id,
    }

    # Adicionar detalhes específicos do tipo de evento ao hash
    # Isso garante que o hash seja único e representativo do evento completo.
    event_type_name_lower = event_instance.event_type.name.lower()

    if event_type_name_lower == 'movimento' or event_type_name_lower == 'movimentação':
        detail = event_instance.movements.first()
        if detail:
            data_to_hash["movement_details"] = {
                "origin_property_id": detail.origin_property_id,
                "destination_property_id": detail.destination_property_id,
                "reason": detail.reason,
                "movement_date": detail.date.isoformat()
            }
    elif event_type_name_lower == 'pesagem':
        detail = event_instance.weighings.first()
        if detail:
            data_to_hash["weighing_details"] = {
                "weight": str(detail.weight), # Decimal para string
                "weighing_date": detail.date.isoformat()
            }
    elif event_type_name_lower == 'vacinação' or event_type_name_lower == 'vacina': # Cobrindo variações
        detail = event_instance.vaccines.first()
        if detail:
            data_to_hash["vacine_details"] = {
                "name": detail.name,
                "manufacturer": detail.manufacturer,
                "batch": detail.batch,
                "validity": detail.validity.isoformat(),
                "dose": str(detail.dose), # Decimal para string
                "next_dose_date": detail.next_dose_date.isoformat() if detail.next_dose_date else None,
            }
    elif event_type_name_lower == 'medicação' or event_type_name_lower == 'medicamento':
        detail = event_instance.medicines.first()
        if detail:
            data_to_hash["medicine_details"] = {
                "name": detail.name,
                "manufacturer": detail.manufacturer,
                "batch": detail.batch,
                "validity": detail.validity.isoformat(),
                "dose": str(detail.dose),
                "next_dose_date": detail.next_dose_date.isoformat() if detail.next_dose_date else None,
                "reason": detail.reason,
                "withdrawal_time": detail.withdrawal_time,
            }
    elif event_type_name_lower == 'reprodução' or event_type_name_lower == 'reproducao':
        detail = event_instance.reproductions.first()
        if detail:
            data_to_hash["reproduction_details"] = {
                "reproduction_type": detail.reproduction_type,
                "male_id": detail.male_id_id, # Acessando o ID do ForeignKey
                "female_id": detail.female_id_id, # Acessando o ID do ForeignKey
                "reproduction_date": detail.date.isoformat(),
                "result": detail.result,
            }
    elif event_type_name_lower == 'abate':
        detail = event_instance.slaughters.first()
        if detail:
            data_to_hash["slaughter_details"] = {
                "slaughter_date": detail.date.isoformat(),
                "location": detail.location,
                "final_weight": str(detail.final_weight),
                "inspection_result": detail.inspection_result,
            }
    elif event_type_name_lower == 'ocorrência especial' or event_type_name_lower == 'ocorrencia especial':
        detail = event_instance.special_occurrences.first()
        if detail:
            data_to_hash["special_occurrences_details"] = {
                "occurrence_type": detail.occurrence_type,
                "description": detail.description,
                "occurrence_date": detail.date.isoformat(),
                "actions_taken": detail.actions_taken,
            }

    # Serializa o dicionário para JSON de forma ordenada para garantir consistência do hash
    # A função default=str lida com tipos como Decimal e datetime que não são serializáveis por padrão
    serialized_data = json.dumps(data_to_hash, sort_keys=True, default=str).encode('utf-8')
    
    return hashlib.sha256(serialized_data).hexdigest()