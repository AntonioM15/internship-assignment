/// <reference types="cypress" />

describe('Dashboard before login', () => {
  beforeEach(() => {
    // Intercept dashboard request
    cy.intercept(
      'GET',
      'http://127.0.0.1:5000/api/v1/dashboard/notifications',
      { statusCode: 401, body: {'status': 'error', 'message': 'Usuario no autorizado. Por favor, inicie sesión.'} }
    ).as('notificationsRequest')
    cy.visitPage('/dashboard')
  })

  it('Checks error message if not logged in', () => {
    cy.get('div:contains("Error:")').should('exist')
  })
})

describe('Dashboard after login', () => {
  beforeEach(() => {
    // Intercept unrelated dashboard request
    cy.intercept(
      'GET',
      'http://127.0.0.1:5000/api/v1/dashboard/notifications',
      { statusCode: 200, body: {'status': 'success', 'message': 'Notifications retrieved successfully', 'data': {}} }
    ).as('notificationsRequest')
    cy.visitPage('/dashboard')
    // Wait for loading text to disappear
    cy.get('div:contains("Cargando...")').should('not.exist')
    cy.wait('@notificationsRequest')
  })

  it('Checks no error message if logged in', () => {
    // Confirm no error on screen
    cy.get('div:contains("Error:")').should('not.exist')
  })
})
