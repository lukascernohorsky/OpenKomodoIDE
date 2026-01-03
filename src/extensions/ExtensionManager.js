// Extension Manager
// This file handles extension management for Komodo IDE

/**
 * Extension Manager
 * Manages extensions and plugins for the IDE
 */

class ExtensionManager {
  constructor() {
    this.extensions = new Map();
    this.plugins = new Map();
    this.addons = new Map();
    this.initialized = false;
  }

  /**
   * Initialize the extension manager
   */
  init() {
    console.log('Initializing Extension Manager');
    this._setupExtensionSystem();
    this._loadCoreExtensions();
    this.initialized = true;
    console.log('Extension Manager initialized');
  }

  /**
   * Setup extension system
   */
  _setupExtensionSystem() {
    // Extension system setup will go here
  }

  /**
   * Load core extensions
   */
  _loadCoreExtensions() {
    // Core extension loading will go here
  }

  /**
   * Register an extension
   */
  registerExtension(name, extension) {
    if (this.extensions.has(name)) {
      console.warn(`Extension ${name} already registered`);
      return false;
    }
    this.extensions.set(name, extension);
    console.log(`Registered extension: ${name}`);
    return true;
  }

  /**
   * Get an extension
   */
  getExtension(name) {
    return this.extensions.get(name);
  }

  /**
   * Register a plugin
   */
  registerPlugin(name, plugin) {
    if (this.plugins.has(name)) {
      console.warn(`Plugin ${name} already registered`);
      return false;
    }
    this.plugins.set(name, plugin);
    console.log(`Registered plugin: ${name}`);
    return true;
  }

  /**
   * Get a plugin
   */
  getPlugin(name) {
    return this.plugins.get(name);
  }

  /**
   * Register an addon
   */
  registerAddon(name, addon) {
    if (this.addons.has(name)) {
      console.warn(`Addon ${name} already registered`);
      return false;
    }
    this.addons.set(name, addon);
    console.log(`Registered addon: ${name}`);
    return true;
  }

  /**
   * Get an addon
   */
  getAddon(name) {
    return this.addons.get(name);
  }

  /**
   * Enable an extension
   */
  enableExtension(name) {
    const extension = this.getExtension(name);
    if (extension && extension.enable) {
      extension.enable();
      return true;
    }
    return false;
  }

  /**
   * Disable an extension
   */
  disableExtension(name) {
    const extension = this.getExtension(name);
    if (extension && extension.disable) {
      extension.disable();
      return true;
    }
    return false;
  }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ExtensionManager;
}

console.log('Extension Manager created successfully');