<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'byte_bitrix' );

/** MySQL database username */
define( 'DB_USER', 'byte' );

/** MySQL database password */
define( 'DB_PASSWORD', '3JADnscvTXPwayH4' );

/** MySQL hostname */
define( 'DB_HOST', 'localhost' );

/** Database Charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The Database Collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );
define('WP_MEMORY_LIMIT','64M');
define( 'WP_DEBUG', false );
/**
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',          'KjS4^hG:@#BTw(lHZObfN?jzVfo^)s[4b7KaQJ}X^7FYeQ^W>C6~8LHdwQvCOIl}' );
define( 'SECURE_AUTH_KEY',   '7*xE*&JAUsm#oe^^K0P@+OP9]_f`Lp>[@d.)1taOXmbH0f;Mc-)pbht9Y7Qv;~Z2' );
define( 'LOGGED_IN_KEY',     'dok<6+DkM6q-i58}DqEX5yTgFh:m(rEKJH#h.&ly^6LPU<e2aEMkn4E09_FGd_+i' );
define( 'NONCE_KEY',         ')!}rIRv7?`LAq|;EEiS8p9~M/E%13jd,kmZ}v#qF![zqgmg780sC.@XqS3|y !r!' );
define( 'AUTH_SALT',         'JpTS~Rr_:I_$mppl-x#eoEy1&<[n^S?A3->$aPdhqat?Q-5hc(7o9!l->~%93; 8' );
define( 'SECURE_AUTH_SALT',  'g}dFx9K0T|{.60wrVP$9nN7y%N[]t0TFqjW;,W>.<d K]zPR|@=|X@X}BGhFx4rW' );
define( 'LOGGED_IN_SALT',    'pIRTN8E-+@rA{Ho#$S2V)RT#M1ZsR[>}m!SJ09)o8pmE}R2p6e6O$Ed IBs&3fOP' );
define( 'NONCE_SALT',        '#1cN;?8.KS2:z#mL9LU+I})zv2ZB9^{oMyw9O7DOmP@5t4*9)4x9b|Tg{r7Z++^w' );
define( 'WP_CACHE_KEY_SALT', '0sOEP~=L8@)C_rT0+na7?O-8bwt8)Pf}yUx)5`Ed~<s?(esNMczg+hkxf9CKSQC:' );

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';




/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) )
	define( 'ABSPATH', dirname( __FILE__ ) . '/' );

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
