/// <reference types="cypress" />

describe('Header Test', () => {
  it('Landing page loads', () => {
    cy.visit('http://localhost:5000/landing')
    cy.contains('Una web para gobernarlos a todos')
  })
})
