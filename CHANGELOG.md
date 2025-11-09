# Changelog

## Version 1.1.0 (2025-11-09)

### Added
- Customizable local port (default: 22)
- Resizable window with minimum size constraints
- Larger font sizes (Microsoft YaHei)
- Larger default window size (650x600)

### Changed
- UI language changed to English
- Improved font rendering with Microsoft YaHei
- Updated all documentation to English
- Fixed port mapping direction (remote → local)

### Fixed
- Corrected mapping direction logic
- Fixed check_existing_mapping to parse local port correctly
- Added current_local_port tracking

## Version 1.0.1 (2025-11-09)

### Fixed
- Fixed NoneType error in check_existing_mapping function
- Added null check for empty output to prevent split() on None
- Fixed GBK encoding errors by adding errors='ignore' parameter
- Improved error handling to always display status correctly

### Improved
- Enhanced exception handling
- Better error messages in logs

## Version 1.0.0 (2025-11-09)

### Features
- Initial release
- Port mapping GUI interface
- Create/delete port mappings
- Auto-detect existing mappings
- IP and port validation
- Admin privilege check
