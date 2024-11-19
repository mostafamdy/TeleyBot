import { getAllBots, getBotsCount } from '@/controllers/bots';
import { Router } from 'express';

const botsRouter = Router();

botsRouter.get('/', getAllBots);
botsRouter.get('/count', getBotsCount);

export default botsRouter;
