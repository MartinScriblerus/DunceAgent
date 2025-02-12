/** @type {import('jest').Config} */
module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'jsdom',
    moduleNameMapper: {
      '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
      '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/__mocks__/fileMock.js',
    },
    setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
    transform: {
      '^.+\\.(ts|tsx)$': 'ts-jest',
      '^.+\\.(js|jsx)$': 'babel-jest',
    },
    testPathIgnorePatterns: ['/node_modules/', '/.next/'],
    moduleFileExtensions: ['js', 'jsx', 'ts', 'tsx', 'json', 'node'],
  };