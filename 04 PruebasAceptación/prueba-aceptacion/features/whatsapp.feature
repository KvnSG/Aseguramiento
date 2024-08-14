Feature: 03 Generar Respuestas y recomendaciones

  Scenario: Enviar un mensaje a PharmaBot
    # Pasos de Navegación
    Given I am on the WhatsApp Web login page
    When I scan the QR code to log in
    And I search for the chat with PharmaBot
    And I open the chat with PharmaBot
    And I type "Tengo dolor de cabeza" into the message box
    And I send the message

    # Pasos de Verificación
    Then the message should be sent to PharmaBot