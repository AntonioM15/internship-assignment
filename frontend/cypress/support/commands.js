// cypress/support/commands.js

Cypress.Commands.add('loginAdmin', () => {
  cy.request('POST', 'http://localhost:5000/api/v1/test_routes/login-admin', {
    email: 'test_admin@email.com'
  })
})
