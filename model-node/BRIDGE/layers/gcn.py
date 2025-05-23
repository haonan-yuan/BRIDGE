import torch
import torch.nn as nn
import torch.nn.functional as F


class GCN(nn.Module):
    def __init__(self, in_ft, out_ft, act=None, bias=True):
        super(GCN, self).__init__()
        self.fc = nn.Linear(in_ft, out_ft, bias=False)
        self.act = nn.PReLU()
        if bias:
            self.bias = nn.Parameter(torch.FloatTensor(out_ft))
            self.bias.data.fill_(0.0)
        else:
            self.register_parameter("bias", None)
        for m in self.modules():
            self.weights_init(m)

    def weights_init(self, m):
        if isinstance(m, nn.Linear):
            torch.nn.init.xavier_uniform_(m.weight.data)
            if m.bias is not None:
                m.bias.data.fill_(0.0)

    def forward(self, input, sparse=True):
        seq = input[0].cuda()
        adj = input[1].cuda()
        seq_fts = self.fc(seq)
        if sparse:
            out = torch.spmm(adj, seq_fts)
        else:
            out = torch.mm(adj.squeeze(dim=0), seq_fts)
        if self.bias is not None:
            out += self.bias
        return self.act(out)
