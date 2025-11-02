/**
 * Environment Configuration
 * Typed configuration object from environment variables
 * with validation and logging
 */

export interface Config {
  // API Configuration
  apiBaseUrl: string;

  // External Services
  googleCloudVisionApiKey: string;
  stripePublicKey: string;
  awsS3Bucket: string;

  // Feature Flags
  enableAnalytics: boolean;
  maintenanceMode: boolean;

  // Environment
  isDevelopment: boolean;
  isProduction: boolean;
  isTest: boolean;
}

/**
 * Validate required environment variables
 * Throws error in production if required vars are missing
 */
function validateConfig(): void {
  const requiredVars = [
    'VITE_API_BASE_URL',
  ];

  const missingVars = requiredVars.filter(
    (varName) => !import.meta.env[varName]
  );

  if (missingVars.length > 0) {
    const errorMessage = `Missing required environment variables: ${missingVars.join(', ')}`;
    
    if (import.meta.env.PROD) {
      throw new Error(errorMessage);
    } else {
      console.warn(`⚠️ ${errorMessage}`);
    }
  }
}

/**
 * Mask sensitive values for logging
 */
function maskValue(value: string): string {
  if (!value || value.length < 8) return '***';
  return `${value.substring(0, 4)}...${value.substring(value.length - 4)}`;
}

/**
 * Get boolean value from environment variable
 */
function getBoolean(value: string | undefined, defaultValue: boolean): boolean {
  if (value === undefined) return defaultValue;
  return value.toLowerCase() === 'true';
}

/**
 * Create configuration object from environment variables
 */
function createConfig(): Config {
  return {
    // API Configuration
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api',

    // External Services
    googleCloudVisionApiKey: import.meta.env.VITE_GOOGLE_CLOUD_VISION_API_KEY || '',
    stripePublicKey: import.meta.env.VITE_STRIPE_PUBLIC_KEY || '',
    awsS3Bucket: import.meta.env.VITE_AWS_S3_BUCKET || '',

    // Feature Flags
    enableAnalytics: getBoolean(import.meta.env.VITE_ENABLE_ANALYTICS, false),
    maintenanceMode: getBoolean(import.meta.env.VITE_MAINTENANCE_MODE, false),

    // Environment
    isDevelopment: import.meta.env.DEV,
    isProduction: import.meta.env.PROD,
    isTest: import.meta.env.MODE === 'test',
  };
}

/**
 * Log configuration in development mode (with masked sensitive values)
 */
function logConfig(config: Config): void {
  if (!config.isDevelopment) return;

  console.group('🔧 Application Configuration');
  console.log('Environment:', import.meta.env.MODE);
  console.log('API Base URL:', config.apiBaseUrl);
  console.log('Google Vision API Key:', maskValue(config.googleCloudVisionApiKey));
  console.log('Stripe Public Key:', maskValue(config.stripePublicKey));
  console.log('AWS S3 Bucket:', config.awsS3Bucket);
  console.log('Enable Analytics:', config.enableAnalytics);
  console.log('Maintenance Mode:', config.maintenanceMode);
  console.groupEnd();
}

// Validate and create configuration
validateConfig();
const config = createConfig();
logConfig(config);

export default config;
