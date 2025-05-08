// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/PausableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";

/**
 * @title AnimalTracking
 * @dev Upgradeable (UUPS), com pausa e registro de eventos críticos on-chain.
 */
contract AnimalTracking is
    Initializable,
    OwnableUpgradeable,
    PausableUpgradeable,
    UUPSUpgradeable
{
    // --- Structs & Eventos ---
    struct CriticEvent {
        uint256 eventId;
        uint256 animalId;
        uint8 eventType;
        string dataHash;
        address registrant;
        bytes32 userHash;
        uint256 timestamp;
    }

    event EventRegistered(
        uint256 indexed animalId,
        uint256 indexed eventId,
        uint8 eventType,
        string dataHash,
        address registrant,
        bytes32 userHash
    );

    // --- Errors customizados ---
    error NotAuthorizedRegistrar();
    error DataHashEmpty();
    error UserHashEmpty();
    error IndexOutOfRange();

    // --- Estados ---
    mapping(uint256 => CriticEvent[]) private eventsByAnimal;
    mapping(address => bool) private authorizedRegistrars;

    // --- Modifiers ---
    modifier onlyRegistrar() {
        if (!authorizedRegistrars[msg.sender]) revert NotAuthorizedRegistrar();
        _;
    }

    // --- Inicialização (substitui constructor) ---
    function initialize() public initializer {
        __Ownable_init();
        __Pausable_init();
        __UUPSUpgradeable_init();

        // Autoriza o deployer como registrador
        authorizedRegistrars[_msgSender()] = true;
    }

    // --- UUPS: controle de quem pode atualizar ---
    function _authorizeUpgrade(address) internal override onlyOwner {}

    // --- Controle de registradores ---
    function addRegistrar(address _registrar) external onlyOwner {
        authorizedRegistrars[_registrar] = true;
    }

    function removeRegistrar(address _registrar) external onlyOwner {
        authorizedRegistrars[_registrar] = false;
    }

    // --- Pause/Unpause ---
    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }

    // --- Registro de eventos (só quando não pausado) ---
    function registerEvent(
        uint256 _eventId,
        uint256 _animalId,
        uint8 _eventType,
        string calldata _dataHash,
        bytes32 _userHash
    ) external onlyRegistrar whenNotPaused
    {
        if (bytes(_dataHash).length == 0) revert DataHashEmpty();
        if (_userHash == bytes32(0))           revert UserHashEmpty();

        CriticEvent memory e = CriticEvent({
            eventId:   _eventId,
            animalId:  _animalId,
            eventType: _eventType,
            dataHash:  _dataHash,
            registrant:_msgSender(),
            userHash:  _userHash,
            timestamp: block.timestamp
        });

        eventsByAnimal[_animalId].push(e);
        emit EventRegistered(_animalId, _eventId, _eventType, _dataHash, _msgSender(), _userHash);
    }

    // --- Leitura de dados ---
    function getEventsByAnimal(uint256 _animalId)
        external
        view
        returns (CriticEvent[] memory)
    {
        return eventsByAnimal[_animalId];
    }

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
        if (_index >= eventsByAnimal[_animalId].length) revert IndexOutOfRange();
        CriticEvent memory ev = eventsByAnimal[_animalId][_index];
        return (
            ev.eventId,
            ev.animalId,
            ev.eventType,
            ev.dataHash,
            ev.registrant,
            ev.userHash,
            ev.timestamp
        );
    }

    function getNumberOfEvents(uint256 _animalId)
        external
        view
        returns (uint256)
    {
        return eventsByAnimal[_animalId].length;
    }

    /**
     * @dev Indica se o contrato está ativo.
     * Agora retorna `true` quando não está pausado.
     */
    function isActive() external view returns (bool) {
        return !paused();
    }
}
