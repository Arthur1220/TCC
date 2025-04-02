// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title AnimalTracking
 * @dev Este contrato registra eventos críticos de animais armazenados on-chain,
 *      utilizando um mapping que relaciona o ID do animal a um array de eventos.
 *      Informações detalhadas ficam off-chain, e somente os dados essenciais (incluindo o hash dos dados)
 *      são armazenados on-chain para garantir imutabilidade e auditabilidade.
 *
 * OBSERVAÇÕES:
 * - O tipo de evento será gerenciado no backend, que repassará um número (uint8) para o contrato.
 * - Não há funcionalidade de pausa; para verificar se o contrato está ativo, há uma função que sempre retorna "true".
 * - Apenas endereços autorizados (registrars) poderão chamar a função registerEvent().
 *   O proprietário (ownable) controla quais endereços estão autorizados.
 */
contract AnimalTracking is Ownable {

    /**
     * @dev Estrutura que armazena informações mínimas sobre um evento crítico.
     * @param eventId ID do evento no banco de dados off-chain.
     * @param animalId ID do animal no banco de dados off-chain.
     * @param eventType Número representando o tipo de evento (definido pelo backend).
     * @param dataHash Hash dos dados do evento armazenados off-chain (por exemplo, SHA-256).
     * @param registrant Endereço que registrou o evento on-chain.
     * @param userHash Hash dos dados do usuário que realizou o registro (não é o endereço).
     * @param timestamp Timestamp do bloco quando o evento foi registrado.
     */
    struct CriticEvent {
        uint256 eventId;
        uint256 animalId;
        uint8 eventType;
        string dataHash;
        address registrant;
        bytes32 userHash;
        uint256 timestamp;
    }

    // Mapping: animalId => array de eventos críticos.
    mapping(uint256 => CriticEvent[]) private eventsByAnimal;

    // Evento emitido sempre que um novo evento crítico é registrado.
    event EventRegistered(
        uint256 indexed animalId,
        uint256 indexed eventId,
        uint8 eventType,
        string dataHash,
        address registrant,
        bytes32 userHash
    );

    // Mapping para controlar quais endereços estão autorizados a registrar eventos.
    mapping(address => bool) private authorizedRegistrars;

    /**
     * @dev Modifier que permite a execução apenas se o chamador estiver autorizado.
     */
    modifier onlyRegistrar() {
        require(authorizedRegistrars[msg.sender] == true, "Not authorized registrar");
        _;
    }

    /**
     * @dev Construtor: Inicializa o contrato e define o proprietário como autorizado.
     */
    constructor() Ownable(msg.sender) {
        authorizedRegistrars[msg.sender] = true;
    }

    /**
     * @dev Permite ao proprietário autorizar um novo registrador.
     * Somente o proprietário (ownable) pode chamar esta função.
     * @param _registrar Endereço a ser autorizado.
     */
    function addRegistrar(address _registrar) external onlyOwner {
        authorizedRegistrars[_registrar] = true;
    }

    /**
     * @dev Permite ao proprietário revogar a autorização de um registrador.
     * Somente o proprietário (ownable) pode chamar esta função.
     * @param _registrar Endereço a ser revogado.
     */
    function removeRegistrar(address _registrar) external onlyOwner {
        authorizedRegistrars[_registrar] = false;
    }

    /**
     * @dev Registra um novo evento crítico on-chain.
     * Somente endereços autorizados podem chamar esta função.
     * @param _eventId O ID do evento no banco de dados off-chain.
     * @param _animalId O ID do animal no banco de dados off-chain.
     * @param _eventType O tipo do evento (como número, repassado pelo backend).
     * @param _dataHash O hash dos detalhes do evento armazenados off-chain.
     * @param _userHash O hash dos dados do usuário que realiza o registro.
     *
     * Requisitos:
     * - _dataHash não deve ser vazio.
     * - _userHash não deve ser zero.
     */
    function registerEvent(
        uint256 _eventId,
        uint256 _animalId,
        uint8 _eventType,
        string calldata _dataHash,
        bytes32 _userHash
    ) external onlyRegistrar {
        require(bytes(_dataHash).length > 0, "Data hash nao pode ser vazio");
        require(_userHash != 0x0, "User hash nao pode ser vazio");

        CriticEvent memory newEvent = CriticEvent({
            eventId: _eventId,
            animalId: _animalId,
            eventType: _eventType,
            dataHash: _dataHash,
            registrant: msg.sender,
            userHash: _userHash,
            timestamp: block.timestamp
        });

        eventsByAnimal[_animalId].push(newEvent);

        emit EventRegistered(
            _animalId,
            _eventId,
            _eventType,
            _dataHash,
            msg.sender,
            _userHash
        );
    }

    /**
     * @dev Retorna todos os eventos críticos de um animal.
     * @param _animalId O ID do animal no banco de dados off-chain.
     * @return Um array de structs CriticEvent.
     */
    function getEventsByAnimal(uint256 _animalId)
        external
        view
        returns (CriticEvent[] memory)
    {
        return eventsByAnimal[_animalId];
    }

    /**
     * @dev Retorna um evento específico de um animal, baseado no índice.
     * @param _animalId O ID do animal.
     * @param _index O índice no array de eventos.
     * @return eventId ID do evento
     * @return animalId ID do animal
     * @return eventType Código do tipo de evento
     * @return dataHash Hash do evento armazenado off-chain
     * @return registrant Endereço que registrou o evento
     * @return userHash Hash do usuário (diferente do address)
     * @return timestamp Timestamp quando o evento foi registrado
     */
    function getEventByIndex(uint256 _animalId, uint256 _index)
        external
        view
        returns (
            uint256 eventId,
            uint256 animalId,
            uint8 eventType,
            string memory dataHash,
            address registrant,
            bytes32 userHash,
            uint256 timestamp
        )
    {
        require(_index < eventsByAnimal[_animalId].length, "Indice fora do intervalo");
        CriticEvent memory e = eventsByAnimal[_animalId][_index];
        return (e.eventId, e.animalId, e.eventType, e.dataHash, e.registrant, e.userHash, e.timestamp);
    }

    /**
     * @dev Retorna o número de eventos registrados para um animal.
     * @param _animalId O ID do animal.
     * @return O número total de eventos.
     */
    function getNumberOfEvents(uint256 _animalId)
        external
        view
        returns (uint256)
    {
        return eventsByAnimal[_animalId].length;
    }

    /**
     * @dev Função para testar se o contrato está ativo.
     * Como não há funcionalidade de pausa, esta função sempre retorna true.
     * @return true, indicando que o contrato está ativo.
     */
    function isActive() external pure returns (bool) {
        return true;
    }
}
