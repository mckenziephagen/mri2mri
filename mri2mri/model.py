import torch
import torch.utils.model_zoo
from .networks import define_net, print_network

MODEL_DICT = {
    't2w2t1w':
    'https://digital.lib.washington.edu/researchworks/bitstream/handle/1773/44486/t2w2t1w_percept-4ba150ef.pth',
    't1w2t2w':
    'https://digital.lib.washington.edu/researchworks/bitstream/handle/1773/44486/t1w2t2w_percept-53951e93.pth'}


class Model():
    def name(self):
        return 'Model'

    def initialize(self, opt):
        self.gpu_ids = opt.gpu_ids
        self.net = define_net(3, 3, opt.model, self.gpu_ids)
        self.load_network(self.net, opt.transform)

        if opt.verbose:
            print('---------- Networks initialized -------------')
            print_network(self.net)
            print('-----------------------------------------------')

    def set_input(self, input):
        # we need to use single_dataset mode
        input_A = input['A']
        if len(self.gpu_ids) > 0:
            input_A = input_A.cuda(self.gpu_ids[0], non_blocking=True)
        self.real_A = input_A

    def forward(self):
        self.fake_B = self.net(self.real_A)

    def load_network(self, network, transform):
        if transform not in MODEL_DICT:
            raise NotImplementedError('%s is not supported' % transform)
        model_path = MODEL_DICT[transform]
        state_dict = torch.utils.model_zoo.load_url(model_path)
        network.load_state_dict(state_dict)
