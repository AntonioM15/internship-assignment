/// <reference types="cypress" />

describe('Header Test', () => {
  beforeEach(() => {
    cy.visitPage('/landing')
  })

  it('Landing page loads', () => {
    cy.contains('Una web para gobernarlos a todos')
  })
})
