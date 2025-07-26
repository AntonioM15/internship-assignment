// cypress/support/commands.js

Cypress.Commands.add('getBaseUrl', () => {
  const isLocal = Cypress.env('ENV') === 'local'
  const url = isLocal ? 'http://localhost:8080' : 'http://localhost:5000'
  return url
})

Cypress.Commands.add('getFullUrl', (path) => {
  return cy.getBaseUrl().then((baseUrl) => {
    const cleanedBase = baseUrl.replace(/\/$/, '')
    const cleanedPath = path.replace(/^\//, '')
    return `${cleanedBase}/${cleanedPath}`
  })
})

Cypress.Commands.add('visitPage', (path) => {
  cy.getFullUrl(path).then((fullUrl) => {
    cy.visit(fullUrl)
  })
})

Cypress.Commands.add('loginAdmin', () => {
  cy.request('POST', 'http://localhost:5000/api/v1/test_routes/login-admin', {
    email: 'test_admin@email.com'
  })
})
