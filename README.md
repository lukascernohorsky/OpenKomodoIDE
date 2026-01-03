# OpenKomodoIDE

OpenKomodoIDE is an open-source implementation of Komodo IDE based on Firefox 140 ESR. This project aims to provide a modern, extensible IDE platform built on web technologies.

## Features

- **Modern Architecture**: Built on Firefox 140 ESR with modern web technologies
- **Extensible**: Designed for easy extension and customization
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Developer-Friendly**: Built with developers in mind

## Getting Started

### Prerequisites

- Node.js (>=14.0.0)
- npm (>=6.0.0)
- Python 3.x
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/OpenKomodo/OpenKomodoIDE.git
   cd OpenKomodoIDE
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build the project:
   ```bash
   npm run build
   ```

4. Run the application:
   ```bash
   npm start
   ```

## Project Structure

```
src/
├── main/              # Main application code
│   ├── application/   # Application entry point
│   └── core/          # Core functionality
├── components/        # Reusable components
├── integrations/      # Integration layers
│   └── firefox/       # Firefox integration
└── tests/             # Test suite
```

## Development

### Running Tests

```bash
npm test
```

### Linting

```bash
npm run lint
```

### Building

```bash
npm run build
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MPL-2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Mozilla Foundation for Firefox
- All contributors and supporters

## Support

For support, please open an issue on the GitHub repository.

## Roadmap

- Complete Firefox 140 ESR integration
- Implement core IDE functionality
- Add extension system
- Improve performance and stability
- Add more language support

## Contact

For more information, please visit our [GitHub repository](https://github.com/OpenKomodo/OpenKomodoIDE).