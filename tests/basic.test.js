// Basic functionality tests
// This file contains basic tests for core functionality

const assert = require('assert');
const { KomodoApp } = require('../src/main/application/App.js');
const { KomodoEngine } = require('../src/main/core/Engine.js');
const { FirefoxIntegration } = require('../src/integrations/firefox/FirefoxIntegration.js');

describe('Basic Functionality Tests', function() {
  let app;
  let engine;
  let firefoxIntegration;

  before(function() {
    // Setup before tests
    app = new KomodoApp();
    engine = new KomodoEngine();
    firefoxIntegration = new FirefoxIntegration();
  });

  describe('KomodoApp', function() {
    it('should initialize correctly', function() {
      assert.strictEqual(app.name, 'Komodo IDE');
      assert.strictEqual(app.version, '12.0');
      assert.strictEqual(app.ready, false);
    });

    it('should initialize when init() is called', function() {
      app.init();
      assert.strictEqual(app.ready, true);
    });
  });

  describe('KomodoEngine', function() {
    it('should initialize correctly', function() {
      assert.strictEqual(engine.initialized, false);
      assert.instanceOf(engine.components, Map);
    });

    it('should initialize when init() is called', function() {
      engine.init();
      assert.strictEqual(engine.initialized, true);
    });
  });

  describe('FirefoxIntegration', function() {
    it('should initialize correctly', function() {
      assert.strictEqual(firefoxIntegration.initialized, false);
      assert.strictEqual(firefoxIntegration.firefoxVersion, '140.0');
      assert.instanceOf(firefoxIntegration.integrationPoints, Set);
    });

    it('should initialize when init() is called', function() {
      firefoxIntegration.init();
      assert.strictEqual(firefoxIntegration.initialized, true);
    });

    it('should be available after initialization', function() {
      firefoxIntegration.init();
      assert.strictEqual(firefoxIntegration.isAvailable(), true);
    });
  });

  after(function() {
    // Cleanup after tests
    app = null;
    engine = null;
    firefoxIntegration = null;
  });
});

console.log('Basic tests created successfully');