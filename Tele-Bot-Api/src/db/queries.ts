export const queries = {
  createBotsTable:
    'CREATE TABLE IF NOT EXISTS bots (id INTEGER PRIMARY KEY AUTOINCREMENT, session TEXT, phone TEXT, messageId INTEGER, joinedDate DATETIME DEFAULT CURRENT_TIMESTAMP)',
  createBannedTable:
    'CREATE TABLE IF NOT EXISTS banned (id INTEGER PRIMARY KEY AUTOINCREMENT, phone TEXT, bannedDate DATETIME DEFAULT CURRENT_TIMESTAMP, joinedDate DATETIME DEFAULT CURRENT_TIMESTAMP)',
  getAllBots: 'SELECT * FROM bots ORDER BY id ASC',
  getAllBanned: 'SELECT * FROM banned',
  addBot: 'INSERT INTO bots (session, phone) VALUES (?, ?)',
  deleteBot: 'DELETE FROM bots WHERE id = ?',
  getBotById: 'SELECT * FROM bots WHERE id = ?',
  getBotByPhone: 'SELECT * FROM bots WHERE phone = ?',
  getBannedBotByPhone: 'SELECT * FROM banned WHERE phone = ?',
  updateMessageId: 'UPDATE bots SET messageId = ? WHERE id = ?',
  banBot: 'INSERT INTO banned (phone, joinedDate) VALUES (?, ?)',
} as const;
