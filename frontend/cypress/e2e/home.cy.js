/// <reference types="cypress" />

describe('Home Test', () => {
  beforeEach(() => {
    cy.visitPage('/landing')
  })

  // ASSETS
  it('Checks if the icons are present', () => {
    cy.get('.icon').should('have.length', 3)
  })

  it('Checks the title', () => {
    cy.get('.title').should('contain', 'Una web para gobernarlos a todos')
  })

  it('Checks the subtitle', function() {
    cy.get('.subtitle').should('contain', 'Empresas, tutores y estudiantes en la misma plataforma')
  })

  // LOGIN
  it('Login form works with valid credentials', () => {
    // Fill login form
    cy.get('.top-right-section input[placeholder="email"]').type('test@example.com')
    cy.get('.top-right-section input[placeholder="contraseña"]').type('password123')

    // Intercept the login request and mock a successful response
    cy.intercept(
      'POST',
      'http://127.0.0.1:5000/api/v1/landing/login',
      { statusCode: 200, body: { 'status': 'success' } }
    ).as('loginRequest')

    // Intercept unrelated dashboard request
    cy.intercept(
      'GET',
      'http://127.0.0.1:5000/api/v1/dashboard/notifications',
      { statusCode: 200, body: {'status': 'success', 'message': 'Notifications retrieved successfully', 'data': {}} }
    ).as('notificationsRequest')

    cy.get('.top-right-section button[type="submit"]').contains('Log in').click({ force: true })
    cy.wait('@loginRequest')
    cy.wait('@notificationsRequest')

    // Check if redirected to dashboard
    cy.url().should('include', '/dashboard')
  })

  it('Login form is not actioned with incomplete credentials - no password', () => {
    cy.get('.top-right-section input[placeholder="email"]').type('incomplete@example.com')
    cy.get('.top-right-section button[type="submit"]').contains('Log in').click({ force: true })

    // Credentials are not sent if missing to fill in one field - check url has not been redirected
    cy.url().should('not.include', '/dashboard')
  })

  it('Login form is not actioned with incomplete credentials - no email', () => {
    cy.get('.top-right-section input[placeholder="contraseña"]').type('password123')
    cy.get('.top-right-section button[type="submit"]').contains('Log in').click({ force: true })

    // Credentials are not sent if missing to fill in one field - check url has not been redirected
    cy.url().should('not.include', '/dashboard')
  })

  it('Login form shows error with invalid credentials', () => {
    cy.get('.top-right-section input[placeholder="email"]').type('invalid@example.com')
    cy.get('.top-right-section input[placeholder="contraseña"]').type('wrongpassword')

    // Intercept the login request and mock an error response
    cy.intercept(
      'POST',
      'http://127.0.0.1:5000/api/v1/landing/login',
      { statusCode: 401, body: { 'status': 'error', 'message': 'Email o contraseña incorrectos' } }
    ).as('loginRequest')

    cy.get('.top-right-section button[type="submit"]').contains('Log in').click({ force: true })
    cy.wait('@loginRequest')
    cy.get('.custom-message').should('contain.text', 'Email o contraseña incorrectos')
  })

  // PASSWORD RECOVERY
  it('Password recovery form works', () => {
    cy.get('.bottom-right-section input[placeholder="email"]').type('recover@example.com')

    // Intercept the password recovery request and mock an error response
    cy.intercept(
      'POST',
      'http://127.0.0.1:5000/api/v1/landing/password-recovery',
      { statusCode: 200, body: { 'status': 'success', 'message': 'Email con instrucciones enviado' } }
    ).as('recoveryRequest')

    cy.get('.bottom-right-section button[type="submit"]').contains('Solicitar').click({ force: true })
    cy.wait('@recoveryRequest')
    cy.get('.custom-message').should('contain.text', 'Email con instrucciones enviado')
  })

  it('Password recovery form is not actioned with imcomplete credentials', () => {
    cy.get('.bottom-right-section button[type="submit"]').contains('Solicitar').click({ force: true })

    // Credentials are not sent if missing to fill in one field - check url has not been redirected
    cy.getFullUrl('/landing').then((fullUrl) => {
      cy.url().should('eq', fullUrl)
    })
  })

  it('Help text contains contact link', () => {
    cy.contains('¿Tienes algún problema?').should('exist')
    cy.contains('Contáctanos').should('have.attr', 'href', '#')
  })
})
