Feature: 03 Generar Respuestas y recomendaciones

  Scenario: No recibe respuesta
    # Pasos de Verificación
    Given I am on the WhatsApp Web login page
    When I scan the QR code to log in
    And I search for the chat with PharmaBot
    And I open the chat with PharmaBot
    And I type "1+1" into the message box
    And I send the message

    # Pasos de Verificación
    Then I should not receive a response from PharmaBot
