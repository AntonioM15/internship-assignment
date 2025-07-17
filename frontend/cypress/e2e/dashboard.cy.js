/// <reference types="cypress" />
const dashboardUrl = 'http://localhost:5000/dashboard'

describe('Dashboard before login', () => {
  beforeEach(() => {
    cy.visit(dashboardUrl)
    // Wait for loading text to disappear
    cy.get('div:contains("Cargando...")').should('not.exist')
  })

  it('Checks error message if not logged in', () => {
    cy.get('div:contains("Error:")').should('exist')
  })
})

describe('Dashboard after login', () => {
  beforeEach(() => {
    cy.loginAdmin()
  })

  it('Checks no error message if logged in', () => {
    // Intercept unrelated call to avoid error
    cy.intercept(
      'GET',
      'http://127.0.0.1:5000/api/v1/dashboard/notifications',
      { statusCode: 200, body: {'status': 'success', 'message': 'Notifications retrieved successfully', 'data': {}} }
    ).as('notificationsRequest')

    cy.visit(dashboardUrl)
    // Wait for loading text to disappear
    cy.get('div:contains("Cargando...")').should('not.exist')
    cy.wait('@notificationsRequest')

    // Confirm no error on screen
    cy.get('div:contains("Error:")').should('not.exist')
  })
})
