import { sendCode, verifyCode } from '@/controllers/auth';
import { Router } from 'express';

const authRouter = Router();

authRouter.post('/send-code', sendCode);
authRouter.post('/verify-code', verifyCode);

export default authRouter;
