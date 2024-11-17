/// <reference types="cypress" />

describe('Home Test', () => {
  it('Landing page loads', () => {
    cy.visit('http://localhost:8080/landing');
    cy.contains('Portal Prácticas de Vuelo');
  });
});
